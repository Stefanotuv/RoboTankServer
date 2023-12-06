# robot_controller.py

# phew
from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.server import redirect
from phew.template import render_template

# app libreary for Servo, Motor, Ultrasonic and Network
from app_lib.network import Network
from app_lib.ultrasonic import ultra
from app_lib.motor_speed import Motor_Speed_Main
from app_lib.servo import Servo

# other generic libraries
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C, SoftI2C
import ujson
import json
import machine
import os
import utime
import sys
import _thread

# Soft reset the MicroPython interpreter




class RobotControllerTankX:
    def __init__(self):
        self.AP_NAME = "PicoRobot"
        self.AP_PASSWORD = "PicoRobot"
        self.AP_DOMAIN = "pipico.net"
        self.TEMPLATE_PATH = "templates"
        self.CONFIG_FILE = "config.json"
        self.FRONT_CAMERA_IP = "192.168.1.161"  # initial value
        self.BACK_CAMERA_IP = "192.168.1.171"  # initial value
        self.IP_ADDRESS = ""
        self.DASHBOARD = 'dashboard_app_tank_x.html'
        self.SPEED = 1 # starting value before reading from settings

#          to use the monitor to dispay the ip address.
#          the usage of the monitor need to be uncommented

#          self.i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=40000)
#          alternative if I2C gives error 
#          self.i2c = SoftI2C(sda=Pin(16), scl=Pin(17), freq=40000)

#          self.oled = SSD1306_I2C(128, 64, self.i2c)

        self.network = Network()
        self.wlan = None  # initialise the wlan that will be used in wifi mode
        self.motor = Motor_Speed_Main()
        # front
        self.front_servo_camera_tilt = Servo(pin=19)
        self.front_servo_camera_pan = Servo(pin=20)

        # back (this may not be installed)
        self.back_servo_camera_tilt = Servo(pin=18)
        self.back_servo_camera_pan = Servo(pin=19)

    def cleanup(self):
        # Cleanup code goes here
#         self.oled.fill(0)
#         self.oled.show()
        pass

    def machine_reset(self):
        # credits to https://github.com/simonprickett/phewap/tree/main
        utime.sleep(1)
        print("Resetting...")
        machine.reset()

    def app_api_reset(self, request):
        # Machine reset code goes here
        value_to_return = "Resetting"
        _thread.start_new_thread(self.machine_reset, ())
        # Return the value before resetting
        return value_to_return

    def setup_mode(self):
        # Setup mode code goes here
        def app_settings_ap(request):
            # request_string = str(request.form)
            if request.method == "POST":
                print("inside post")
                ap_wifi = request.data.get('ap_wifi')
                ssid = request.data.get('ssid')
                password = request.data.get('password')
                front_camera_ip = request.data.get('front_camera_ip')
                back_camera_ip = request.data.get('back_camera_ip')
                speed = request.data.get('speed')

                # os.stat(CONFIG_FILE)
                print("inside post before deleting file")
                os.remove(self.CONFIG_FILE)
                with open(self.CONFIG_FILE, "w") as f:
                    #             with open(CONFIG_FILE) as f:
                    file_string = {"ap_wifi": ap_wifi,
                                   "ssid": ssid,
                                   "password": password,
                                   "front_camera_ip": front_camera_ip,
                                   "back_camera_ip": back_camera_ip,
                                   "speed": speed}

                    self.FRONT_CAMERA_IP = front_camera_ip
                    self.BACK_CAMERA_IP = back_camera_ip
                    print(f'file_string: {file_string}')
                    print("inside with")
                    json.dump(file_string, f)
                    print('file dumped')
                    f.close()
                    print('file closed')
                #           add logic to check the save or the restart and code the restarting routine

                print("here")
                print(f'request data: {request.data}')
                submit = request.data.get('submit')
                if submit == 'save_restart':
                    print('inside save restart')
                    self.machine_reset()

                elif submit == 'save':
                    print('save')
                    wifi_networks = self.network.scan_networks(ap)
                    print(f'wifi_networks: {wifi_networks}')

                    wifi_options = self.network.wifi_networks_options(wifi_networks)
                    print(f'wifi_options: {wifi_options}')

                    return render_template(f"{self.TEMPLATE_PATH}/settings.html", ip=self.IP_ADDRESS, saved=1,
                                           domain=self.AP_DOMAIN,
                                           ap_wifi=ap_wifi, speed=speed,
                                           ssid=ssid, password=password, front_camera_ip=front_camera_ip,
                                           back_camera_ip=back_camera_ip, wifi_networks_options=wifi_options)
                else:
                    # restart routine
                    pass

            elif request.method == "GET":

                # os.stat(CONFIG_FILE)
                with open(self.CONFIG_FILE) as f:
                    file = json.load(f)
                    ap_wifi = file["ap_wifi"]
                    ssid = file["ssid"]
                    password = file["password"]
                    front_camera_ip = file["front_camera_ip"]
                    back_camera_ip = file["back_camera_ip"]
                    speed = file["speed"]
                    f.close()
                wifi_networks = self.network.scan_networks(ap)
                print(f'wifi_networks: {wifi_networks}')

                wifi_options = self.network.wifi_networks_options(wifi_networks)
                print(f'wifi_options: {wifi_options}')

                return render_template(f"{self.TEMPLATE_PATH}/settings.html", ip=self.IP_ADDRESS, domain=self.AP_DOMAIN,
                                       ap_wifi=ap_wifi,
                                       ssid=ssid,
                                       speed=speed,
                                       password=password, front_camera_ip=front_camera_ip,
                                       back_camera_ip=back_camera_ip,
                                       wifi_networks_options=wifi_options)

            else:
                pass
            pass

        def ap_app(request):
            print("ap_app")
            #wifi_networks = self.network.scan_networks(ap)
            #print(f'wifi_networks: {wifi_networks}')

            #wifi_options = network.wifi_networks_options(wifi_networks)
            #print(f'wifi_options: {wifi_options}')

            return render_template(f'{self.TEMPLATE_PATH}/{self.DASHBOARD}', ip=self.IP_ADDRESS, ap_wifi="ap",
                                   front_camera_ip=self.FRONT_CAMERA_IP, back_camera_ip=self.BACK_CAMERA_IP)


        def ap_catch_all(request):
            print("CATCH ALL")

            print(f"request headers: {request.headers}")
            #             host = request.headers.get("host")
            # return render_template(f"{TEMPLATE_PATH}/redirect.html", domain=AP_DOMAIN)
            #             if host != self.AP_DOMAIN:
            #                 print(f"index AP domain different host:{host} AP_DOMAIN:{self.AP_DOMAIN}")
            # return render_template(f"{TEMPLATE_PATH}/redirect.html", domain=AP_DOMAIN)
            #                 return redirect("http://192.168.4.1/")
            return "Not found.", 404

        # print("adding routes")
        server.add_route("/", handler=ap_app, methods=["GET"])
        #         server.add_route("/config", handler=ap_config, methods=["GET", "POST"])
        server.add_route("/settings", handler=app_settings_ap, methods=["GET", "POST"])
        # print("adding set_callback")
        server.add_route("/motor", handler=self.app_motor_move, methods=["GET"])
        server.add_route("/camera", handler=self.app_camera_move, methods=["GET"])
        server.add_route("/distance", handler=self.app_distance, methods=["GET"])

        server.add_route("/api/settings", handler=self.app_api_settings, methods=["GET", "POST"])
        server.add_route("/api/settings/reset", handler=self.app_api_reset, methods=["GET", "POST"])
        server.add_route("/api/controls", handler=self.app_api_controls, methods=["GET", "POST"])
        
        
        server.set_callback(ap_catch_all)

        # print("adding access_point")
        ap = access_point(self.AP_NAME, self.AP_PASSWORD)

        ip = ap.ifconfig()[0]

        print(f'ip:{ip}')
        # self.oled.fill(0)
        # self.oled.text("SSID: PicoRobot", 0, 0)
        # self.oled.text("Pwd: PicoRobot", 0, 10)
        # self.oled.text("use 192.168.4.1", 0, 20)
        # self.oled.show()

        # add code to visualise that the system started as a AP

        dns.run_catchall(ip)

    def application_mode(self):
        # Application mode code goes here
        print("Entering application mode.")

        # onboard_led = machine.Pin("LED", machine.Pin.OUT)



        server.add_route("/", handler=self.app_app, methods=["GET", "POST"])
        server.add_route("/motor", handler=self.app_motor_move, methods=["GET"])
        server.add_route("/camera", handler=self.app_camera_move, methods=["GET"])
        server.add_route("/distance", handler=self.app_distance, methods=["GET"])
        server.add_route("/settings", handler=self.app_settings, methods=["GET", "POST"])

        server.add_route("/api", handler=self.app_api, methods=["GET", "POST"])
        server.add_route("/api/controls", handler=self.app_api_controls, methods=["GET", "POST"])
        server.add_route("/api/settings", handler=self.app_api_settings, methods=["GET", "POST"])
        server.add_route("/api/distance", handler=self.app_distance, methods=["GET"])
        server.add_route("/api/settings/reset", handler=self.app_api_reset, methods=["GET", "POST"])
        server.set_callback(self.app_catch_all)
        pass



    def app_api_controls(self,request):
        if request.method == "POST":
            control = request.data.get('control')
            value = request.data.get('value')
            print(f'API call received')
            print(f'control: {control}')
            print(f'value: {value}')

            if control == "up": # camera controls
                self.app_api_camera_move(value)
                pass

            if control == "down": # motors controls
                self.app_api_motor_move(value)
                pass

        return "received"

    def app_api_camera_move(self,move):
        if move == "up":
            self.front_servo_camera_tilt.up()
        elif move == "down":
            self.front_servo_camera_tilt.down()
        elif move == "left":
            self.front_servo_camera_pan.left()
        elif move == "right":
            self.front_servo_camera_pan.right()
        else:
            self.front_servo_camera_pan.center()
            self.front_servo_camera_tilt.center()
        return ""
        pass

    def app_api_motor_move(self,move):
        if move == "up":
            self.motor.move_forward_continue(speed=int(self.SPEED))
        elif move == "down":
            self.motor.move_backward_continue(speed=int(self.SPEED))
        elif move == "left":
            self.motor.move_left_continue(speed=int(self.SPEED))
        elif move == "right":
            self.motor.move_right_continue(speed=int(self.SPEED))
        else:
            self.motor.move_stop()
            print("stop")
        return ""
    def app_camera_move(self,request):
        # query_string example
        # query_string: camera_control = down?front_back = front
        camera_control = (request.query_string.split("=")[1]).split("?")[0]

        front_back = request.query_string.split("=")[2]

        print(f'camera_control:{camera_control}')
        print(f'front_back:{front_back}')
        # onboard_led.toggle()
        if camera_control == "up":
            # front_servo_camera_tilt.up() if front_back == "front" else back_servo_camera_tilt.up()
            if front_back == "front":
                self.front_servo_camera_tilt.up()
            else:
                self.back_servo_camera_tilt.up()
        elif camera_control == "down":
            if front_back == "front":
                self.front_servo_camera_tilt.down()
            else:
                self.back_servo_camera_tilt.down()
        elif camera_control == "left":
            if front_back == "front":
                self.front_servo_camera_pan.left()
            else:
                self.back_servo_camera_pan.left()
        elif camera_control == "right":
            if front_back == "front":
                self.front_servo_camera_pan.right()
            else:
                self.back_servo_camera_pan.right()
        elif camera_control == "center":
            if front_back == "front":
                self.front_servo_camera_pan.center()
                self.front_servo_camera_tilt.center()
            else:
                self.back_servo_camera_pan.center()
                self.back_servo_camera_tilt.center()
        else:
            print("mouse down?")
        return ""

    def app_motor_move(self,request):
        print("motor")
        # onboard_led.toggle()

        motor_control = request.query_string.split("=")[1]
        print(f'motor_control:{motor_control}')

        if motor_control == "up":
            self.motor.move_forward()
        elif motor_control == "down":
            self.motor.move_backward()
        elif motor_control == "left":
            self.motor.move_left()
        elif motor_control == "right":
            self.motor.move_right()
        elif motor_control == "up_continue":
            self.motor.move_forward_continue(speed=int(self.SPEED))
        elif motor_control == "down_continue":
            self.motor.move_backward_continue(speed=int(self.SPEED))
        elif motor_control == "left_continue":
            self.motor.move_left_continue(speed=int(self.SPEED))
        elif motor_control == "right_continue":
            self.motor.move_right_continue(speed=int(self.SPEED))
        else:
            self.motor.move_stop()
            print("stop")
        return ""
    def app_app(self,request):
        return render_template(f"{self.TEMPLATE_PATH}/{self.DASHBOARD}", ip=self.IP_ADDRESS, ap_wifi="wifi",
                               front_camera_ip=self.FRONT_CAMERA_IP, back_camera_ip=self.BACK_CAMERA_IP)

    def app_settings(self,request):
        # request_string = str(request.form)
        if request.method == "POST":
            print("inside post")
            ap_wifi = request.data.get('ap_wifi')
            ssid = request.data.get('ssid')
            password = request.data.get('password')
            front_camera_ip = request.data.get('front_camera_ip')
            back_camera_ip = request.data.get('back_camera_ip')
            speed = request.data.get('speed')

            # os.stat(CONFIG_FILE)
            print("inside post before deliting file")
            os.remove(self.CONFIG_FILE)
            with open(self.CONFIG_FILE, "w") as f:
                #             with open(CONFIG_FILE) as f:
                file_string = {"ap_wifi": ap_wifi,
                               "ssid": ssid,
                               "password": password,
                               "front_camera_ip": front_camera_ip,
                               "back_camera_ip": back_camera_ip,
                               "speed": speed}

                self.FRONT_CAMERA_IP = front_camera_ip
                self.BACK_CAMERA_IP = back_camera_ip
                self.SPEED = speed
                print(f'file_string: {file_string}')
                print("inside with")
                json.dump(file_string, f)
                print('file dumped')
                f.close()
                print('file closed')
            #           add logic to check the save or the restart and code the restarting routine

            print("here")
            print(f'request data: {request.data}')
            submit = request.data.get('submit')
            if submit == 'save_restart':
                print('inside save restart')
                self.machine_reset()

            elif submit == 'save':
                print('save')
                wifi_networks = self.network.scan_networks(self.wlan)
                print(f'wifi_networks: {wifi_networks}')

                wifi_options = self.network.wifi_networks_options(wifi_networks)
                print(f'wifi_options: {wifi_options}')

                return render_template(f"{self.TEMPLATE_PATH}/settings.html", ip=self.IP_ADDRESS, saved=1,
                                       domain=self.AP_DOMAIN,
                                       ap_wifi=ap_wifi, speed=speed,
                                       ssid=ssid, password=password, front_camera_ip=front_camera_ip,
                                       back_camera_ip=back_camera_ip, wifi_networks_options=wifi_options)
            else:
                # restart routine
                pass

        elif request.method == "GET":

            # os.stat(CONFIG_FILE)
            with open(self.CONFIG_FILE) as f:
                file = json.load(f)
                ap_wifi = file["ap_wifi"]
                ssid = file["ssid"]
                password = file["password"]
                front_camera_ip = file["front_camera_ip"]
                back_camera_ip = file["back_camera_ip"]
                speed = file["speed"]
                f.close()
            wifi_networks = self.network.scan_networks(self.wlan)
            print(f'wifi_networks: {wifi_networks}')

            wifi_options = self.network.wifi_networks_options(wifi_networks)
            print(f'wifi_options: {wifi_options}')

            return render_template(f"{self.TEMPLATE_PATH}/settings.html", ip=self.IP_ADDRESS, domain=self.AP_DOMAIN,
                                   ap_wifi=ap_wifi,
                                   ssid=ssid,
                                   speed=speed,
                                   password=password, front_camera_ip=front_camera_ip,
                                   back_camera_ip=back_camera_ip,
                                   wifi_networks_options=wifi_options)

        else:
            pass
        pass


    def app_distance(self,request):
        print("api distance call")
        if request.method == "GET":
            print("get call")
            distance = ultra()
            print(f'distance: {distance}')
            string = {'distance': distance.split(' ')[0]}
            print(f'string: {string}')
            value = ujson.dumps(string)
            return value
        else:
            return "not recognised"

    # def app_api(self,request):
    #     print("api")
    #     if request.method == "POST":
    #
    #         print("POST")
    #         print(request.data)  # {'scaledY': 0.8568848, 'scaledX': 0.5155081, 'joypad': 'top'}
    #
    #         scaledY = request.data.get('scaledY')
    #         scaledX = request.data.get('scaledX')
    #         mulX = 0
    #         mulY = 0
    #         # print(f'{api}')
    #         if abs(scaledX) > 0.7:
    #             mulX = 1
    #         elif abs(scaledX) > 0.3:
    #             mulX = 2
    #         elif abs(scaledX) > 0:
    #             mulX = 3
    #
    #         if abs(scaledY) > 0.7:
    #             mulY = 1
    #         elif abs(scaledY) > 0.3:
    #             mulY = 2
    #         elif abs(scaledY) > 0:
    #             mulY = 3
    #
    #         horizontal = int(20 * mulX)
    #         vertical = int(20 * mulY)
    #         print(f'horizontal: {horizontal}')
    #         print(f'vertical: {vertical}')
    #
    #         joypad = request.data.get('joypad')
    #
    #         if joypad == 'top':  # camera servos
    #
    #             if scaledX > 0 and scaledY > 0:
    #                 self.front_servo_camera_pan.right(input=horizontal)
    #                 self.front_servo_camera_tilt.up(input=vertical)
    #                 print("scaledX > 0 and scaledY > 0")
    #
    #             elif scaledX < 0 and scaledY > 0:
    #                 self.front_servo_camera_pan.left(input=horizontal)
    #                 self.front_servo_camera_tilt.up(input=vertical)
    #                 print("scaledX < 0 and scaledY > 0")
    #
    #             elif scaledX < 0 and scaledY < 0:
    #                 self.front_servo_camera_pan.left(input=horizontal)
    #                 self.front_servo_camera_tilt.down(input=vertical)
    #                 print("scaledX < 0 and scaledY < 0")
    #
    #             elif scaledX > 0 and scaledY < 0:
    #                 self.front_servo_camera_pan.right(input=horizontal)
    #                 self.front_servo_camera_tilt.down(input=vertical)
    #                 print("scaledX > 0 and scaledY , 0")
    #             else:
    #                 print("pass")
    #                 pass
    #             # front_servo_camera_pan.center()
    #             # front_servo_camera_tilt.center()
    #
    #         elif joypad == 'bottom':  # motors
    #
    #             if scaledX > 0 and scaledY > 0:
    #                 self.motor.move_forward_api()
    #                 self.motor.move_right_api()
    #                 print("scaledX > 0 and scaledY > 0")
    #
    #             elif scaledX < 0 and scaledY > 0:
    #                 self.motor.move_forward_api()
    #                 self.motor.move_left_api()
    #                 print("scaledX < 0 and scaledY > 0")
    #
    #             elif scaledX < 0 and scaledY < 0:
    #                 self.motor.move_backward_api()
    #                 self.motor.move_left_api()
    #                 print("scaledX < 0 and scaledY < 0")
    #
    #             elif scaledX > 0 and scaledY < 0:
    #                 self.motor.move_right_api()
    #                 self.motor.move_backward_api()
    #                 print("scaledX > 0 and scaledY , 0")
    #             else:
    #                 self.motor.move_stop_api()
    #                 print("stop")
    #                 pass
    #
    #             pass
    #         else:
    #             pass
    #         return 'success'
    #
    #     elif request.method == "GET":
    #         print("GET")
    #         query_string = request.query_string  # contains all the info post api?key1=value1&key2=value2 -> key1=value1&key2=value2
    #         print(f'query_string:{query_string}')
    #         return 'success'
    #
    #     else:
    #         pass
    #
    #     return ('check for errors')

    def app_api_settings(self,request):
        if request.method == "GET":
            # read the parameters from the file
            os.stat(self.CONFIG_FILE)  # verify if it is required ...
            with open(self.CONFIG_FILE) as f:
                file = json.load(f)
                ap_wifi = file["ap_wifi"]
                ssid = file["ssid"]
                speed = file["speed"]
                password = file["password"]
                front_camera_ip = file["front_camera_ip"]
                back_camera_ip = file["back_camera_ip"]
                file_string = {"ap_wifi": ap_wifi,
                               "ssid": ssid,
                               "password": password,
                               "front_camera_ip": front_camera_ip,
                               "speed": speed,
                               "back_camera_ip": back_camera_ip}
                f.close()
        elif request.method == "POST":
            ap_wifi = request.data.get('ap_wifi')
            ssid = request.data.get('ssid')
            password = request.data.get('password')
            front_camera_ip = request.data.get('front_camera_ip')
            back_camera_ip = request.data.get('back_camera_ip')
            speed = request.data.get('speed')
            file_string = {"ap_wifi": ap_wifi, "ssid": ssid,
                           "password": password, "front_camera_ip": front_camera_ip,
                           "back_camera_ip": back_camera_ip,
                           "speed":speed }

            os.remove(self.CONFIG_FILE)
            with open(self.CONFIG_FILE, "w") as f:
               json.dump(file_string, f)
               f.close()
            print(f'file_string:{file_string}')
            # add write to file
        else:
            pass

        print("api config")

        return f'{file_string}'

    def app_catch_all(self,request):
        return "Not found.", 404
    def start(self):
        print('start routine launched')
        try:
            # First check the configuration file for the mode to start
            os.stat(self.CONFIG_FILE)
            with open(self.CONFIG_FILE) as f:
                print('file opened')
                config = json.load(f)
                print('file read')
                ap_wifi = config["ap_wifi"]
                print(f'ap_wifi: {ap_wifi}')
                f.close()

            if ap_wifi == "ap":
                print(f'mode ap launched')
                self.AP_mode()
            else:
                print(f'mode wifi launched')
                self.WiFi_mode(ssid=config["ssid"], password=config["password"])
        except Exception as e:
            # If no valid configuration is found, or there's an exception, start in AP mode.
            print(f'mode ap launched by exception')
            print(f'exception:{e}')
            self.AP_mode()

    def AP_mode(self):
        # Start in Access Point (AP) mode
        self.setup_mode()
        server.run()

    def WiFi_mode(self, ssid, password):
        # Start in Wi-Fi mode

        wlan = connect_to_wifi(ssid, password)

        if not is_connected_to_wifi():
            # Failed to connect to Wi-Fi, switch to AP mode
            self.AP_mode()
            server.run()
        else:
            ip_address = wlan.ifconfig()[0]
            self.wlan = wlan
            self.IP_ADDRESS = ip_address
            print(f'ip address: {ip_address}')
#             self.oled.fill(0)
#             self.oled.text("WiFi mode", 0, 0)
#             self.oled.text(ip_address, 0, 15)
#             self.oled.show()
            self.application_mode()
            server.run()