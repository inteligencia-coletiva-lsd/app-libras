from flask import (Flask, jsonify, request)
import json
import os
import random
import urllib2
import urllib
import pbclient
import requests

app = Flask(__name__)

VIDEOS_DIR = "/home/thyagofas/web_dev/pybossa/app-libras/static_libras/libras-videos/"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_BLENDER_DIR = os.path.join(APP_DIR, "scripts-blender")
BLEND_FILE = os.path.join(SCRIPTS_BLENDER_DIR, "mulher05_iK_14_05.blend")
MOV_PONTUAL_SCRIPT = os.path.join(SCRIPTS_BLENDER_DIR, "movPontual.py")

pbclient.set('endpoint', "http://localhost:8080/pybossa")


@app.route( "/getCurrIpAddr" )
def getCurrIpAddr():
    return jsonify( curr_usr_ip = getUserIp() )

@app.route( "/validateTask", methods = ['POST'] )
def validateTask():
    task_info = json.loads( request.data )

    app_id = pbclient.find_app( short_name = "librasdictionary" )[0].id

    # sets the task as completed
    requests.put( "%s/api/task/%s?api_key=%s" % 
                 ( "http://localhost:8080/pybossa", task_info["task_id"], "53b8465d-91b0-4286-b2d8-834fbd89e194" ), 
                 data = json.dumps( dict( state = "completed" ) ) )

    return jsonify( resultado = None )

@app.route( "/getLastTaskrun", methods = ['POST'] )
def getLastTaskrun():
    task_id = json.loads( request.data )    
    app_id = pbclient.find_app( short_name = "librasdictionary" )[0].id
    taskruns_for_task_id = pbclient.find_taskruns( app_id, task_id = task_id )
    if len( taskruns_for_task_id ) != 0:
        return jsonify( lastTaskrun = taskruns_for_task_id[-1].info )
    return jsonify( lastTaskrun = None )

@app.route( "/userReport", methods = ['POST'] )
def userReport():
    info = json.loads( request.data )
    current_user_id = info["current_user_id"]
    app_id = pbclient.find_app( short_name = "librasdictionary" )[0].id
    current_user_ip = getUserIp();
    all_task_runs = getAllTaskRuns( app_id ) 
    # TODO comparar a quantidade de tarefas disponiveis com a quantidade de tarefas completas
    tasks_amount = getTasksAmount( app_id ) * 5

    user_task_runs = dict()
    user_task_runs_amount = 0
    user_signs = dict()
    signs_validated = list()
    signs_improved = list()
    users_amount = 0
    comunity_average = 0
    user_average = 0
    overall_progress = 0
    last_time = "Nunca"
    if( len( all_task_runs ) > 0 ):
        user_task_runs = getUserTaskRuns( app_id, current_user_id, current_user_ip )
        user_signs = getUserSigns( user_task_runs )
        user_task_runs_amount = len( user_task_runs ) - len( user_signs['skips'] )        
        users_amount = getUsersAmount( all_task_runs )
        all_task_runs_amount = len( all_task_runs )
        
        if ( users_amount ) == 1:
            comunity_average = all_task_runs_amount
        else:
            comunity_average = ( all_task_runs_amount - user_task_runs_amount ) / ( float( users_amount - 1 ) )

        user_average = round( user_task_runs_amount / float( comunity_average ), 2 )
        
        if ( user_average < 0.5 ) and ( user_task_runs_amount != 0 ):
            user_average = 1
        elif user_average >= 0.5 and user_average < 1:
            user_average = 1 + user_average
        elif user_average >= 1 and user_average < 1.5:
            user_average = 2 + (user_average - 1)
        elif user_average >= 1.5:
            user_average = 3

        overall_progress = round( ( all_task_runs_amount / float(tasks_amount) ) * 100, 2 )
        comunity_average = round( comunity_average, 2 )

        if ( user_task_runs_amount > 0 ):
            last_time = user_task_runs[-1].finish_time.split("T")[0]
 
        signs_validated = getSignsValidated( all_task_runs )

        signs_improved = getSignsImproved( all_task_runs )

    return jsonify( user_signs = user_signs, signs_validated = signs_validated, signs_improved = signs_improved, last_time = last_time, overall_progress = overall_progress, user_average = user_average, user_task_runs_amount = user_task_runs_amount, comunity_average = comunity_average )


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

def getUserSigns( user_task_runs ):
    user_skips = list()
    user_configs = list()
    user_validations = list() 
    user_improvements = list()
    for task_run in user_task_runs:
    
        if 'final_state' in task_run.info:
            user_skips.append( task_run.info['signal_name'] )
        else:
            if( task_run.info['configuration'] == "yes" ):
                user_configs.append( task_run.info['signal_name'] )

            if( task_run.info['validation'] == "yes" ):
                user_validations.append( task_run.info['signal_name'] )

            if( task_run.info['improvement'] == "yes" ):
                user_improvements.append( task_run.info['signal_name'] )

    user_signs = dict( configs = user_configs, validations = user_validations, improvements = user_improvements, skips = user_skips )

    return user_signs

def getSignsValidated( all_taskruns ):
    signs_validated = list()
    for taskrun in all_taskruns:
    
        if 'final_state' in taskrun.info:
            pass
        elif ( taskrun.info['validation'] == "yes" ):
            signs_validated.append( taskrun.info['signal_name'] )

    return signs_validated

def getSignsImproved( all_taskruns ):
    signs_improved = list()
    for taskrun in all_taskruns:
        if 'final_state' in taskrun.info:
            pass
        elif ( taskrun.info['improvement'] == "yes" ):
            signs_improved.append( taskrun.info['signal_name'] )

    return signs_improved

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
     #avatar_file = signal_name + ".webm"
     avatar_file = signal_name + ".webm"
     return jsonify(rendered_video=avatar_file, exitcode=exitcode)

if __name__ == "__main__":
    app.run(debug=True)

