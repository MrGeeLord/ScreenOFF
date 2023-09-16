from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import ctypes
import os
import subprocess
import win32gui
import win32con
import win32api, win32con
def screen_on():
    ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)
    # os.system('nircmd\\nircmd.exe monitor on')
    move_cursor()


def move_cursor():
    x, y = (0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)


def screen_off():
    """
    Function to turn off the screen.
    """
    return win32gui.SendMessage(win32con.HWND_BROADCAST,
                            win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)

def setsounddevice():
    vbs_script_path = r'C:\Users\GeeLord\django_projects\ScreenOFF\venv\Scripts\SSD.vbs'

    try:
        process = subprocess.Popen(['cscript', vbs_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Error occurred while running the VBScript:")
            print("Standard Output:")
            print(stdout.decode())
            print("Standard Error:")
            print(stderr.decode())
    except Exception as e:
        print("An error occurred:", str(e))
    # exe_path = r'C:\Program Files\set sound device\SSD.exe'
    # arg = '77719997777hidden'
    #
    # try:
    #     # Run the executable with the specified argument
    #     subprocess.run([exe_path, arg], check=True)
    #     print("Execution successful.")
    # except FileNotFoundError:
    #     print(f"Executable '{exe_path}' not found.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Execution failed with return code {e.returncode}.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

def button_view(request):
    if request.method == 'POST':
        if 'screenon' in request.POST:
            # Call the screen_on function
            screen_on()
            # output = screen_on()
            # return HttpResponse(f'Screen is ON. Script output: {output}')
        elif 'screenoff' in request.POST:
            # Call the screen_off function
            screen_off()
            # output = screen_off()
            # return HttpResponse(f'Screen is OFF. Script output: {output}')
        elif 'shutdown' in request.POST:
            # os.system("shutdown /p")
            # subprocess.run(["shutdown", "/s", "/t", "0"])
            # Define the flags for different shutdown operations
            # Call the ExitWindowsEx function to shut down the computer
            # ctypes.windll.user32.ExitWindowsEx(1, 0)
            os.system('shutdown /s /t 0')

        elif 'restart' in request.POST:
            # ctypes.windll.user32.ExitWindowsEx(2 | 4, 0)
            os.system('shutdown /r /t 0')
        elif 'setsounddevice' in request.POST:
            setsounddevice()
    # return HttpResponseRedirect('main/index.html')
    return render(request, 'main/index.html')