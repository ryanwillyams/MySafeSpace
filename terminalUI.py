import time

if __name__ == "__main__":
    print("MySafeSpace")

    option = ""
    while True:
        # Different Security options
        option = (input("----------------------------------\n"
                        "Options\n"
                        "----------------------------------\n"
                        "1. Change password requirements\n"
                        "2. Change password for user(s)\n"
                        "3. Change sudoers\n"
                        "4. Configure SSH\n"
                        "5. Disable services\n"
                        "6. View logs\n"
                        "0. Quit Program\n"
                        "----------------------------------\n"
                        "Select an option: "))
        print("----------------------------------\n")

        match option:
            case "1":
                print("Not yet implemented.")
            case "2":
                print("Not yet implemented.")
            case "3":
                print("Not yet implemented.")
            case "4":
                print("Not yet implemented.")
            case "5":
                print("Not yet implemented.")
            case "6":
                print("Not yet implemented.")
            case "0":
                print("Quitting program.")
                exit()
            case _:
                print("Invalid entry.")
        
        time.sleep(1)