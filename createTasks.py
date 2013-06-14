#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import json
from optparse import OptionParser
import pbclient
import re
import random

def get_videos_ids():
    signs_video = {}
    with open( 'libras_signs_videos.json', 'rb' ) as fp:
        signs_video = json.load( fp )
    
    return signs_video

def contents(filename):
    return file(filename).read()
    
if __name__ == "__main__":
    # Arguments for the application
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    # URL where PyBossa listens
    parser.add_option("-s", "--server", dest="api_url",
                      help="PyBossa URL http://domain.com/", metavar="URL",
                      default="http://localhost/pybossa")
    # API-KEY
    parser.add_option("-k", "--api-key", dest="api_key",
                      help="PyBossa User API-KEY to interact with PyBossa",
                      metavar="API-KEY")
    # Create App
    parser.add_option("-c", "--create-app", action="store_true",
                      dest="create_app",
                      help="Create the application",
                      metavar="CREATE-APP")
    # Update template for tasks and long_description for app
    parser.add_option("-t", "--update-template", action="store_true",
                      dest="update_template",
                      help="Update Tasks template",
                      metavar="UPDATE-TEMPLATE")

    # Update tasks question
    parser.add_option("-q", "--update-tasks",
                      dest="update_tasks",
                      help="Update Tasks n_answers",
                      metavar="UPDATE-TASKS")

    parser.add_option("-x", "--extra-task", action="store_true",
                      dest="add_more_tasks",
                      help="Add more tasks",
                      metavar="ADD-MORE-TASKS")

    # Modify the number of TaskRuns per Task
    # (default 30)
    parser.add_option("-n", "--number-answers",
                      type="int",
                      dest="n_answers",
                      help="Number of answers per task",
                      metavar="N-ANSWERS",
                      default=30)

    parser.add_option("-a", "--application-config",
                      dest="app_config",
                      help="Application config file",
                      metavar="APP-CONFIG",
                      default="app.json")

    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    (options, args) = parser.parse_args()

    # Load app details
    try:
        with file(options.app_config) as app_json:
            app_config = json.load(app_json)
    except IOError as e:
        print "application config file is missing! Please create a new one"
        exit(1)

    pbclient.set('endpoint', options.api_url)

    if not options.api_key:
        parser.error("You must supply an API-KEY to create an \
                      applicationa and tasks in PyBossa")
    else:
        pbclient.set('api_key', options.api_key)

    if options.verbose:
        print('Running against PyBosssa instance at: %s' % options.api_url)
        print('Using API-KEY: %s' % options.api_key)

    def find_app_by_short_name():
        return pbclient.find_app(short_name=app_config['short_name'])[0]

    def setup_app():
        app = find_app_by_short_name()
        app.long_description = contents('long_description.html')
        app.info['task_presenter'] = contents( "template.html" )
        app.info['thumbnail'] = app_config['thumbnail']
        app.info['tutorial'] = contents('tutorial.html')

        pbclient.update_app(app)
        return app
    
    def create_video_task(app, signal_name, video_id, question):
        # Data for the tasks
        task_info = dict(question=question,
                         n_answers=options.n_answers,
			 signal_name=signal_name,
                         video_id=video_id)
        pbclient.create_task(app.id, task_info)

    if options.create_app:
        pbclient.create_app(app_config['name'],
                            app_config['short_name'],
                            app_config['description'])

        app = setup_app()

        # First of all we get the URL photos
        # Then, we have to create a set of tasks for the application
        # For this, we get first the photo URLs from Flickr

        videos_ids = get_videos_ids()
        question = app_config['question']
        #questions = [ "Com quantas m&atilde;os se faz o sinal?", 
        #              "Escolha &eacute; a orienta&ccedil;&atilde;o inicial da palma da m&atilde;o direita?",
        #              "Selecione &eacute; o ponto de articula&ccedil;&atilde;o da m&atilde;o direita?",
        #              "Com que express&atilde;o facial se faz o sinal?",
        #              "Escolha a forma inicial da m&atilde;o direita." ]
        
        #videoId_questions_dict = dict() 
        #for video_id in videos_ids:
        #    videoId_questions_dict[ video_id ] = questions[:]
        
        # Batch creation
        #for i in xrange(1):
            #videosId_keys = videoId_questions_dict.keys()
            #while True:
            #    if len( videosId_keys ) == 0:
            #        break
                
            #    videoId_key = random.choice( videosId_keys )
            #    questions_values = videoId_questions_dict[ videoId_key ]  
            #    if len( questions_values ) != 0:
            #        question = random.choice( questions_values )
            #        create_video_task( app, videoId_key, question )
            #        videoId_questions_dict[ videoId_key ].remove( question )
            #    else:
            #        videosId_keys.remove( videoId_key )
                
#            for question in questions:
#                for video_id in videos_ids:
#                    create_video_task( app, video_id, question)
        for k,v in videos_ids.iteritems():
          create_video_task( app, k, v, question)
      
    else:
        if options.add_more_tasks:

            app = find_app_by_short_name()
            videos_ids = get_videos_ids()
            question = "Com quantas m&atilde;os se faz o sinal?"
            for k,v in iteritems():
              create_video_task(app, k, v, question)

    if options.update_template:
        print "Updating app template"
        # discard return value
        setup_app()

    if options.update_tasks:
        print "Updating task n_answers"
        app = find_app_by_short_name()
        n_tasks = 0
        offset = 0
        limit = 100
        tasks = pbclient.get_tasks(app.id, offset=offset, limit=limit)
        while tasks:
            for task in tasks:
                print "Updating task: %s" % task.id
                if ('n_answers' in task.info.keys()):
                    del(task.info['n_answers'])
                task.n_answers = int(options.update_tasks)
                pbclient.update_task(task)
                n_tasks += 1
            offset = (offset + limit)
            tasks = pbclient.get_tasks(app.id, offset=offset, limit=limit)
        print "%s Tasks have been updated!" % n_tasks

    if not options.create_app and not options.update_template\
            and not options.add_more_tasks and not options.update_tasks:
        parser.error("Please check --help or -h for the available options")

