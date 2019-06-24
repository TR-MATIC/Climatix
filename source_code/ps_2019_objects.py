import requests
import time
import csv


class CLX_Tester(object):
    def __init__(self, config_path="2_config.txt"):
        self.__config_path = config_path
        self.__configuration = {}
        self.__ao_list = []
        self.__config_OK = False
        self.__path_OK = False
        self.__data_OK = False
        self.__consistency_OK = False
        self.__synchronized = False
        self.__progress = 0
        self.__layout = ""
        self.__end = ""


    @property
    def config_path(self):
        return self.__config_path


    @property
    def config_OK(self):
        return self.__config_OK


    @property
    def path_OK(self):
        return self.__path_OK


    @property
    def data_OK(self):
        return self.__data_OK


    @property
    def consistency_OK(self):
        return self.__consistency_OK


    def print_center(self, text, lenght=66):
        layout = "|{:^" + str(lenght-2) + "}|"
        print(layout.format(text))
        # Total lenght of 66 characters means space of 64 characters closed between two vertical frames ||


    def print_line(self, lenght=66):
        line = "+" + "-" * (lenght-2) + "+"
        print(line)


    def print_progress(self, symbol, lenght=66, mode="PyCharm", endchar=""):
        # symbol == "End" for ending the progress bar, filling the gap and closing the vertical frame |
        # symbol == "." for rows skipped by initial synchronization
        # symbol == "s" for rows sent properly
        # symbol == "x" for rows sent, but rejected

        # First 13 characters are used for timestamp, 1 last character is spacing from the vertical frame |
        # max_bar defines, how long the actual progress bar could possibly be.
        max_bar = (lenght-2) - (13+1)
        if mode == "PyCharm":
            self.__layout = ""
        if self.__progress == 0:
            timestamp = time.strftime("%m.%d %H:%M")
            self.__layout = "| " + timestamp + " " + symbol
            print(self.__layout, end=endchar)
            self.__progress += 1
        elif symbol == "End":
            the_gap = max_bar - (self.__progress % max_bar)
            self.__layout = self.__layout + " " * the_gap + " |"
            print(self.__layout)
        elif self.__progress % max_bar == 0:
            #print(" |")
            timestamp = time.strftime("%m.%d %H:%M")
            self.__layout = self.__layout + " |"
            print(self.__layout)
            self.__layout = "| " + timestamp + " " + symbol
            print(self.__layout, end=endchar)
            self.__progress += 1
        else:
            self.__layout = self.__layout + symbol
            print(self.__layout, end=endchar)
            self.__progress += 1

    def invite(self):
        timestamp = time.strftime("%Y.%m.%d  %H:%M")
        # Prior to starting the script, the location of config file must be given.
        print()
        self.__config_path = input(
            "Please, enter full path of the TXT configuration file : \n"
            "(Hint: copy from Windows explorer.)\n"
            )
        print()
        # Now starting the real operation of the script.
        self.print_line()
        self.print_center("Starting Climatix Tester Script.")
        self.print_center(timestamp)
        self.print_line()
        return True


    def load_config(self):
        self.print_line()
        self.print_center("Loading configuration.")
        try:
            config_file = open(self.__config_path, "r")
        except FileNotFoundError:
            self.print_center("Configuration file not found.")
        except:
            self.print_center("Unknown configuration file error.")
        else:
            text_len = len(self.__config_path)
            if text_len > 35:
                display_path = self.__config_path[0:3] + "..." + self.__config_path[text_len-29:text_len]
            else:
                display_path = self.__config_path
            self.print_center("File " + display_path + " loaded successfully.")
            for line in config_file:
                line = line.rstrip("\n")
                key, value = line.split(":", maxsplit=1)
                self.__configuration.update({key: value})
            config_file.close()
            self.__config_OK = True
        finally:
            self.print_line()
        if self.__config_OK:
            self.print_center("Checking configuration.")
            for key, item in self.__configuration.items():
                if key in ["date", "time", "path"]:
                    text_len = len(item)
                    if text_len > 54:
                        display_item = item[0:3] + "..." + item[text_len - 48:text_len]
                    else:
                        display_item = item
                    self.print_center(key + " : " + display_item)
            if "path" not in self.__configuration.keys():
                self.print_center("Parameter \"path\" not specified correctly.")
                self.print_center("HINT: Provide correct path, example: data_file.csv")
            elif "addr" not in self.__configuration.keys():
                self.print_center("Parameter \"addr\" not specified correctly.")
                self.print_center("HINT: Provide correct IP address, example: 192.168.10.101")
            elif "name" not in self.__configuration.keys():
                self.print_center("Parameter \"name\" not specified correctly.")
                self.print_center("HINT: Provide correct user name, example: JSON")
            elif "pasw" not in self.__configuration.keys():
                self.print_center("Parameter \"pasw\" not specified correctly.")
                self.print_center("HINT: Provide correct password, example: SBTMaster")
            elif "pin" not in self.__configuration.keys():
                self.print_center("Parameter \"pin\" not specified correctly.")
                self.print_center("HINT: Provide correct PIN, example: 1234")
            else:
                self.print_center("Configuration OK.")
                self.__path_OK = True
            self.print_line()
        return True


    def load_data(self):
        self.print_center("Loading CSV data.")
        try:
            data_file = open(self.__configuration["path"], "r")
        except FileNotFoundError:
            self.print_center("CSV file not found.")
        except:
            self.print_center("Unknown CSV file error.")
        else:
            text_len = len(self.__configuration["path"])
            if text_len > 35:
                display_path = self.__configuration["path"][0:3] + "..." + self.__configuration["path"][text_len - 29:text_len]
            else:
                display_path = self.__configuration["path"]
            self.print_center("File " + display_path + " loaded successfully.")
            csv_content = csv.reader(data_file, delimiter=";")
            self.__data_OK = True
        finally:
            self.print_line()

        if self.__data_OK:
            self.print_center("Checking data consistency.")
            row_len = 0
            row_len_past = 0
            for cnt, row in enumerate(csv_content):
                row_len = len(row)
                if "" in row:
                    self.__consistency_OK = False
                    break
                if cnt >= 1:
                    if row_len == row_len_past:
                        self.__consistency_OK = True
                    else:
                        self.__consistency_OK = False
                        break
                if cnt >= 2:
                    hh_mm_ss_list = row[0].split(":")
                    if len(hh_mm_ss_list) == 3:
                        self.__consistency_OK = True
                    else:
                        self.__consistency_OK = False
                        break
                    if "" in hh_mm_ss_list:
                        self.__consistency_OK = False
                        break
                row_len_past = row_len
            if not self.__consistency_OK:
                self.print_center("CSV data inconsistent.")
                self.print_center("HINT: Check row number {}.".format(str(cnt+1)))
                self.print_center("Time must be always given in hh:mm:ss format.")
                self.print_center("Number of entries must be equal in all rows.")
                self.print_center("Empty cells in CSV file are not accepted.")
            if self.__consistency_OK:
                self.print_center("CSV content is correct.")
            self.print_line()
            data_file.close()
        return True


    def climatix_url(self):
        climatix_url = "http://" + self.__configuration["addr"] + "/jsongen.html"
        return climatix_url


    def climatix_auth(self):
        climatix_auth = (self.__configuration["name"], self.__configuration["pasw"])
        return climatix_auth


    def climatix_params(self, values_list=[]):
        climatix_params = {"fn": "write"}
        ao_val_list = []
        for cnt, value in enumerate(values_list):
            if "," in value:
                value = value.replace(",",".")
            ao_val_list.append(self.__ao_list[cnt] + ";" + value)
        climatix_params.update({"oa": ao_val_list})
        climatix_params.update({"pin": self.__configuration["pin"]})
        return climatix_params


    def time_compare(self, time_in_sec):
        system_clock = time.strftime("%H:%M:%S")
        [hh, mm, ss] = system_clock.split(":")
        system_clock_in_sec = 3600 * int(hh) + 60 * int(mm) + int(ss)
        if time_in_sec < system_clock_in_sec:
            synchronization = -1
        elif time_in_sec == system_clock_in_sec:
            synchronization = 0
        elif time_in_sec > system_clock_in_sec:
            synchronization = 1
        else:
            pass
        return synchronization


    def send_request(self):
        self.print_center("Starting Climatix communication.")

        data_file = open(self.__configuration["path"], "r")
        csv_content = csv.reader(data_file, delimiter=";")

        values_list = []
        for cnt, row in enumerate(csv_content):
            if cnt == 1:
                # cnt == 0 is generally skipped, that's human-readable 1st header line in the CSV file.
                # cnt == 1 means actually the second line, with BASE64 aObjM references.
                # That line is stored as __ao_list property.
                raw_list = row
                raw_list.pop(0)
                self.__ao_list = raw_list
            elif cnt >= 2:
                # From this row the real data starts. That will be sent to the controller.
                # The data is read from CSV first and prepared for sending.
                [hh, mm, ss] = row[0].split(":")
                time_in_sec = 3600 * int(hh) + 60 * int(mm) + int(ss)
                raw_list = row
                raw_list.pop(0)
                values_list = raw_list
                climatix_params = self.climatix_params(values_list)
                # Then the data must be synchronized. Normally it's out of synchronization, when the script starts.
                # As a result, the CSV track must be pulled to the point of synchronization.
                # For example CSV track starts at 00:00 but script is launched at 08:25,
                # hence first CSV line with time >= 08:25 must be found in the beginning.
                if not self.__synchronized:
                    synchronization = self.time_compare(time_in_sec)
                    if synchronization < 0:
                        self.print_progress(".")
                        continue
                        # Continue FOR loop and check next line
                    elif synchronization >= 0:
                        self.__synchronized = True
                        # Bravo! Initial synchronization is done.

                # Now check for precise synchronization
                if self.__synchronized:
                    synchronization = self.time_compare(time_in_sec)
                    while synchronization != 0:
                        time.sleep(0.050)
                        synchronization = self.time_compare(time_in_sec)
                        # Stay in this loop and check every 50ms if that's the right time
                        # to pull the trigger on communication request.
                try:
                    climatix_get = requests.get(self.climatix_url(), auth=self.climatix_auth(), params=climatix_params, timeout=0.500)
                except requests.exceptions.Timeout:         # Timeout exception, late response, no connection, bad IP
                    response = "T"
                except requests.exceptions.ConnectionError: # Connection error exception
                    response = "C"
                except:                                     # Unknow exception
                    response = "X"
                else:
                    if climatix_get.status_code == 200:
                        if "states" in climatix_get.text:   # Possible data error, out of range, bad type etc.
                            response = "D"
                        elif "Error" in climatix_get.text:  # Possible PIN error
                            response = "P"
                        else:                               # Success!
                            response = "s"
                    elif climatix_get.status_code == 401:   # Unauthorized, bad name or pass
                        response = "U"
                    elif climatix_get.status_code == 404:   # Not Found
                        response ="F"
                    elif climatix_get.status_code >= 500:   # HTTP Server errors 5xx
                        response = "5"
                    elif climatix_get.status_code >= 400:   # HTTP Client errors 4xx
                        response = "4"
                    elif climatix_get.status_code >= 300:   # HTTP Redirections
                        response = "3"
                    elif climatix_get.status_code >= 200:   # HTTP Information
                        response = "2"
                    else:                                   # Unknown status
                        response = "?"
                self.print_progress(response)
            else:
                pass
        self.print_progress("End")
        self.print_line()
        data_file.close()
        return True
