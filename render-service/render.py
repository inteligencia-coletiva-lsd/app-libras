from flask import (Flask, jsonify, request)
import json
import os
import random
import urllib2
import urllib
import pbclient

app = Flask(__name__)

VIDEOS_DIR = "/home/thyagofas/web_dev/pybossa/app-libras/static/libras-videos/"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_BLENDER_DIR = os.path.join(APP_DIR, "scripts-blender")
BLEND_FILE = os.path.join(SCRIPTS_BLENDER_DIR, "mulher05_iK_14_05.blend")
MOV_PONTUAL_SCRIPT = os.path.join(SCRIPTS_BLENDER_DIR, "movPontual.py")

pbclient.set('endpoint', "http://localhost:8080/pybossa")

# TODO
@app.route( "/userReport", methods = ['POST'] )
def userReport():
    info = json.loads(request.data)
    current_user_id = info["current_user_id"]
    app_id = pbclient.find_app( short_name = "librasdictionary" )[0].id
    current_user_ip = getUserIp();
    all_task_runs = getAllTaskRuns( app_id ) 
    tasks_amount = getTasksAmount( app_id ) * 5

    user_task_runs = dict()
    user_signs = []
    users_amount = 0
    comunity_average = 0
    user_average = 0
    overall_progress = 0
    if( len(all_task_runs) > 0 ):
        user_task_runs = getUserTaskRuns( app_id, current_user_id, current_user_ip )
        user_task_runs_amount = len(user_task_runs)
        user_signs = getUserSigns( user_task_runs, current_user_id, current_user_ip )
        users_amount = getUsersAmount( all_task_runs )
        all_task_runs_amount = len( all_task_runs )
        comunity_average = all_task_runs_amount / float(users_amount)
        user_average = round( user_task_runs_amount / comunity_average, 2 )
        
        if ( user_average < 0.5 ) and ( user_task_runs_amount != 0 ):
            user_average = 1
        elif user_average >= 0.5 and user_average < 1:
            user_average = 1 + user_average
        elif user_average >= 1 and user_average < 1.5:
            user_average = 2 + (1 - user_average)
        elif user_average >= 1.5:
            user_average = 3      

        overall_progress = round( ( all_task_runs_amount / float(tasks_amount) ) * 100, 2 )

        if ( user_task_runs_amount > 0 ):
            last_time = user_task_runs[-1].finish_time.split("T")[0]
        else:
            last_time = "Nunca"

    return jsonify( user_signs = user_signs, last_time = last_time, overall_progress = overall_progress, user_average = user_average )


def getUserIp():
    return request.remote_addr

def getTasksAmount( app_id ):
    return len( pbclient.find_tasks( app_id ) )

def getAllTaskRuns( app_id ):
    return pbclient.find_taskruns( app_id )

def getUserTaskRuns( app_id, user_id, current_user_ip ):
    if user_id is None:
        return pbclient.find_taskruns( app_id, user_ip = current_user_ip )        
    return pbclient.find_taskruns( app_id, user_id = user_id )

def getUserSigns( all_task_runs, user_id, current_user_ip ):
    user_signs = []
    for task_run in all_task_runs:
        if ( user_id is None ):
            if( task_run.user_ip == current_user_ip ):
                user_signs.append( task_run.info['signal_name'] )            
        elif( user_id == task_run.user_id ):
            user_signs.append( task_run.info['signal_name'] )
    return user_signs

def getUsersAmount( all_task_runs ):
    users = set()
    for task_run in all_task_runs:
        if (task_run.user_id is None):
            users.add( task_run.user_ip )
        else:
            users.add( task_run.user_id )
    return len( users )

@app.route("/render", methods=['POST'])
def render():
     parameters = json.loads(request.data)
     random_id = str(random.getrandbits(64))     
     signal_name = parameters['signal_name'] + random_id
     user_id = "user_id"

     print "THE SIGNAL NAME IS: " + signal_name

     right_hand = parameters['right']
     left_hand = parameters['left']

     path_dir = VIDEOS_DIR + 'pontualDir' + random_id
     path_esq = VIDEOS_DIR + 'pontualEsq' + random_id

     # mao direita
     try:
	     f = open(path_dir, 'w')
	     f.write(right_hand['CONF_MAO'] + '\n')
	     f.write(right_hand['ORIENT_PALMA'] + '\n')
	     f.write(right_hand['PONTO_ARTIC'] + '\n')
	     f.write(parameters['QTD_MAOS'] + '\n')
	     f.write(signal_name + '\n')
	     f.write(user_id + '\n')
     except IOError: 
	print("Error de IO!")
     except KeyError:
	print("Error de KEY!")
     finally:
	f.close()
 
     # mao esquerda
     try:
	     f = open(path_esq, 'w')
	     if len(left_hand) == 0:
	        f.write('Nenhum\n')
	     else:
	        f.write(left_hand['CONF_MAO'] + '\n')
	     	f.write(left_hand['ORIENT_PALMA'] + '\n')
	     	f.write(left_hand['PONTO_ARTIC'] + '\n')
	     f.write(parameters['EXP_FACIAL'] + '\n')
     except IOError: 
	print("Error de IO!")
     except KeyError:
	print("Error de KEY!")
     finally:
	f.close()

     cmd = "cd " + SCRIPTS_BLENDER_DIR + "; blender -b " + BLEND_FILE + " -o " + VIDEOS_DIR + " -P " + MOV_PONTUAL_SCRIPT + " " + path_dir + " " + path_esq
     exitcode = os.system(cmd)
     avatar_file = signal_name + ".webm"

     return jsonify(rendered_video=avatar_file, exitcode=exitcode)

if __name__ == "__main__":
    app.run(debug=True)

