import os
import shutil
import schedule
import time


def backup(src: str, dst: str) -> None:
    dst += "backup.txt"
    print("Backup Time!")
    shutil.copyfile(src, dst)


def schedule_daily_backup(input_time: str, src: str, dst: str) -> None:
    dst += "daily" + str(time.time())
    schedule.every().day.at(input_time).do(backup, src, dst)
    print(f"Backup scheduled for {input_time} every day")


def schedule_weekly_backup(day: str, input_time: str, src: str, dst: str) -> None:
    dst += "weekly" + str(time.time())
    match day.lower():
        case "sunday":
            schedule.every().sunday.at(input_time).do(backup, src, dst)
        case "monday":
            schedule.every().monday.at(input_time).do(backup, src, dst)
        case "tuesday":
            schedule.every().tuesday.at(input_time).do(backup, src, dst)
        case "wednesday":
            schedule.every().wednesday.at(input_time).do(backup, src, dst)
        case "thursday":
            schedule.every().thursday.at(input_time).do(backup, src, dst)
        case "friday":
            schedule.every().friday.at(input_time).do(backup, src, dst)
        case "saturday":
            schedule.every().saturday.at(input_time).do(backup, src, dst)
        case _:
            print("Wrong input, not a day.")
    print(f"Backup scheduled for {day} every week")


def schedule_monthly_backup(src: str, dst: str) -> None:
    dst += "monthly" + str(time.time())
    schedule.every(4).weeks.do(backup, src, dst)
    print(f"Monthly backup scheduled.")


if __name__ == "__main__":
    source = input("Enter a file to backup: ")
    destination = input("Enter a source to backup to: ") + "/"
    input_time = input("Enter a time in 24h format: ")
    day = input("Enter a day for weekly backup: \n(Sunday/Monday/Tuesday/Wednesday/Thursday/Friday/Saturday)\n")

    schedule_daily_backup(input_time, source, destination)
    schedule_weekly_backup(day, input_time, source, destination)
    schedule_monthly_backup(source, destination)
    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
        time.sleep(1)
