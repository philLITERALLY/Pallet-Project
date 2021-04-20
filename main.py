'''This module handles the main threads'''

import threading        # threading

# my modules
import info_logger      # logger
info_logger.init()      # logger needs loaded
import handle_config    # module to handle config settings
handle_config.init()    # config settings need loaded

import layouts          # UI Layouts
import gui              # gui handler
import worker_thread    # main thread

if __name__ == '__main__':
   
    window = layouts.window # UI Window
    threads = []            # array to hold threads
    
    # collect all threads
    threads.append(threading.Thread(target=worker_thread.main, args=(window,), daemon=True))

    # start all threads
    for thread in threads:
        thread.start()

    # The function that builds the UI and listens for events
    gui.main(window)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    info_logger.shutdown()

    print('Exiting Program')