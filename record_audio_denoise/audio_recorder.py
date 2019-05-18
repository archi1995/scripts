import subprocess
import os
import time
import glob


def status():

    try:

        result = subprocess.check_output(['bash', '-c', 'audio-recorder -c status']).decode('UTF-8').strip('\n')

    except subprocess.CalledProcessError:

        return 'not_launched'

    return result


def start():

    subprocess.check_output(['bash', '-c', 'audio-recorder -c start']).decode('UTF-8')


def stop():

    subprocess.check_output(['bash', '-c', 'audio-recorder -c stop']).decode('UTF-8')


def notify(message, file):

    path_to_dir = os.path.dirname(os.path.abspath(__file__))

    subprocess.check_output(['notify-send', str(message), '-t', '3000', '-i', f'{path_to_dir}/{file}'])


def denoise():

    list_of_files = glob.glob('/home/archi/Audio/*.mp3')  # * means all if need specific format then *.csv
    if list_of_files:

        latest_file = max(list_of_files, key=os.path.getctime)
        latest_file_clean_mp3 = latest_file.strip('.mp3') + '_clean' + '.mp3'
        noize_reduction_value = '0.29'

        subprocess.check_output(['bash', '-c', f'sox {latest_file} {latest_file_clean_mp3} noisered /home/archi/Audio/noise_profile_file {noize_reduction_value}']).decode('UTF-8')
        os.remove(latest_file)


if __name__ == '__main__':

    status = status()
    print(status)

    if status == 'on':

        message = 'stop'
        file = 'img/blue.png'

        stop()
        time.sleep(2)
        denoise()

        notify(message=message, file=file)

    elif status == 'off':

        message = 'start'
        file = 'img/red.png'

        start()
        notify(message=message, file=file)

    elif status == 'not_launched':

        message = 'Launch recorder!'
        file = 'img/not_launched.png'

        notify(message=message, file=file)
