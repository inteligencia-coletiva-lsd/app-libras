from flask import (Flask, jsonify, request)
import json
import os
import random

app = Flask(__name__)

VIDEOS_DIR = "/home/adabriand/pybossa_apps/app-libras/static/"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_BLENDER_DIR = os.path.join(APP_DIR, "scripts-blender")
BLEND_FILE = os.path.join(SCRIPTS_BLENDER_DIR, "mulher05_iK_14_05.blend")
MOV_PONTUAL_SCRIPT = os.path.join(SCRIPTS_BLENDER_DIR, "movPontual.py")

@app.route("/", methods=['POST'])
def render():

     parameters = json.loads(request.data)
     random_id = str(random.getrandbits(64))
     signal_name = parameters['signal_name'] + random_id
     user_id = 'userId'

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

