import requests
import pycountry_convert
import flagpy
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

api_key = "YOUR API KEY HERE" # Read the "IMPORTANT!!!" file for more info
width = 330
height = 180
flag_width, flag_height = 60, 30
flag_coords = (240, 5)
weather_width = weather_height = 120
weather_coords = (190, 45)
sign_limit = 20

weather_label_info = ["City: ", "Country: ", "Geo coords: ", "Weather: ", "Temperature: ", "Pressure: ", "Wind: ", "Clouds: "]
weather_info = ["-", "-", "-", "-", "-", "-", "-", "-"]

def update_weather_info():
    for index, label in enumerate(weather_labels):
        label.config(text=weather_label_info[index] + weather_info[index])

def kelvin_to_celcius(temperature):
    return temperature - 272.15

def reset():
    global weather_info, flag_label, weather_label, weather_img_obj, weather_img, flag_img_obj, flag_img

    city_entry.delete(0, END)
    weather_info = ["-", "-", "-", "-", "-", "-", "-", "-"]
    update_weather_info()

    flag_img_obj = Image.open("images/no image.png")
    flag_img_obj = flag_img_obj.resize((flag_width, flag_height))
    flag_img = ImageTk.PhotoImage(flag_img_obj)
    flag_label.config(image=flag_img)

    weather_img_obj = Image.open("images/no image.png")
    weather_img_obj = weather_img_obj.resize((weather_width, weather_height))
    weather_img = ImageTk.PhotoImage(weather_img_obj)
    weather_label.config(image=weather_img)

def get_info(city):
    global weather_info, weather_label, weather_img_obj, weather_img, flag_img_obj, flag_img

    try:
        weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")

        weather_img_req = requests.get(f"http://openweathermap.org/img/wn/{weather.json()['weather'][0]['icon']}@2x.png")
        with open("images/weather.png", "wb") as f:
            f.write(weather_img_req.content)

        weather_img_obj = Image.open("images/weather.png")
        weather_img_obj = weather_img_obj.resize((weather_width, weather_height))
        weather_img = ImageTk.PhotoImage(weather_img_obj)
        weather_label.config(image=weather_img)

        flag_img_req = flagpy.get_flag_img(pycountry_convert.country_alpha2_to_country_name(weather.json()['sys']['country'], cn_name_format='default'))
        flag_img_req.save("images/flag.png")

        flag_img_obj = Image.open("images/flag.png")
        flag_img_obj = flag_img_obj.resize((flag_width, flag_height))
        flag_img = ImageTk.PhotoImage(flag_img_obj)
        flag_label.config(image=flag_img)

        weather_info[0] = f"{weather.json()['name']}"
        weather_info[1] = f"{pycountry_convert.country_alpha2_to_country_name(weather.json()['sys']['country'], cn_name_format='default')}"
        weather_info[2] = f"[{weather.json()['coord']['lat']}, {weather.json()['coord']['lon']}]"
        if len(weather.json()['weather'][0]['description']) <= sign_limit:
            weather_info[3] = f"{weather.json()['weather'][0]['description']}"
        else:
            weather_info[3] = f"{weather.json()['weather'][0]['main'].lower()}"
        weather_info[4] = f"{round(kelvin_to_celcius(weather.json()['main']['temp']), 1)} °C"
        weather_info[5] = f"{weather.json()['main']['pressure']} hpa"
        weather_info[6] = f"{weather.json()['wind']['speed']} m/s"
        weather_info[7] = f"{weather.json()['clouds']['all']} %"
        update_weather_info()
    except:
        reset()
        messagebox.showerror("Error", """An error occurred\nCheck if you wrote the city name correctly\nAnd if you're connected to the internet""")

    city_entry.delete(0, END)

root = Tk()
root.title("Weather App")
root.geometry(f"{width}x{height}")
root.iconbitmap("images/icon.ico")
root.resizable(False, False)
root.configure(background="lightgrey")

city_label = Label(root, text="City:", background="lightgrey")
city_label.place(x=5, y=5)

city_entry = Entry(root, width=20)
city_entry.place(x=40, y=6)

search_btn = Button(root, text="Search", fg="white", bg="royalblue", height=1, command=lambda: get_info(city_entry.get()))
search_btn.place(x=170, y=3)

weather_labels = [Label(root, text=weather_label_info[i] + weather_info[i], background="lightgrey") for i in range(8)]
for index, label in enumerate(weather_labels):
    label.place(x=3, y=30 + (index * 18))

flag_img_obj = Image.open("images/no image.png")
flag_img_obj = flag_img_obj.resize((flag_width, flag_height))
flag_img = ImageTk.PhotoImage(flag_img_obj)
flag_label = Label(root, background="lightgrey", image=flag_img)
flag_label.place(x=flag_coords[0], y=flag_coords[1])

weather_img_obj = Image.open("images/no image.png")
weather_img_obj = weather_img_obj.resize((weather_width, weather_height))
weather_img = ImageTk.PhotoImage(weather_img_obj)
weather_label = Label(root, background="lightgrey", image=weather_img)
weather_label.place(x=weather_coords[0], y=weather_coords[1])

root.bind("<Return>", lambda x: get_info(city_entry.get()))

root.mainloop()