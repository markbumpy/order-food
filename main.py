import customtkinter
import sqlite3
from tkinter import *

from tkinter import messagebox

from PIL import Image, ImageTk

app = customtkinter.CTk()
app.title('My restaurant')
app.geometry('700x700')
app.config(bg='#000')
app.resizable(False, False)

variable1 = StringVar()
variable2 = StringVar()
variable3 = StringVar()

font1 = ('Courier New', 22, 'bold')

# function to get the quantity from the database

def get_quantity():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT quantity FROM restaurant')
    results = c.fetchall()

    global food1_quantity
    global food2_quantity
    global food3_quantity

    food1_quantity = results[0][0]
    food2_quantity = results[1][0]
    food3_quantity = results[2][0]
    # if the quantity of the food is finished it tells the customer that the product is sold out
    if food1_quantity == 0:
        variable1.set('0')
        p1_quantity.destroy()
        p1_state_label = customtkinter.CTkLabel(p1_frame, font=font1, text='Sold out', text_color='#f00', bg_color='#000', width=100)
        p1_state_label.place(x=50, y=270)

        # if the product is not 0 the customer is able to buy the product
    else:
        list1 = [str(i) for i in range(food1_quantity+1)]
        p1_quantity.configure(values=list1)
        p1_quantity.set('0')
        # this is the same thing but for the second product
    if food2_quantity == 0:
        variable2.set('0')
        p2_quantity.destroy()
        p2_state_label = customtkinter.CTkLabel(p2_frame, font=font1, text='Sold out', text_color='#f00', bg_color='#000', width=100)
        p2_state_label.place(x=50, y=270)
    else:
        list2 = [str(i) for i in range(food2_quantity+1)]
        p2_quantity.configure(values=list2)
        p2_quantity.set('0')
    # the same thing but for the third product
    if food3_quantity == 0:
        variable3.set('0')
        p3_quantity.destroy()
        p3_state_label = customtkinter.CTkLabel(p3_frame, font=font1, text='Sold out', text_color='#f00', bg_color='#000', width=100)
        p3_state_label.place(x=50, y=270)
    else:
        list3 = [str(i) for i in range(food3_quantity+1)]
        p3_quantity.configure(values=list3)
        p3_quantity.set('0')

# function that handles the checkout button


def checkout():
    if food1_quantity == 0 and food2_quantity == 0 and food3_quantity == 0:
        messagebox.showerror('opps your cart is empty')
    else:
        if customer_entry.get():
            conn = sqlite3.connect('restaurant.db')
            c = conn.cursor()
            quantity1 = int(variable1.get())
            quantity2 = int(variable2.get())
            quantity3 = int(variable3.get())
            c.execute("UPDATE restaurant SET quantity = ? WHERE id = ?", (food1_quantity - quantity1, 1))
            c.execute("UPDATE restaurant SET quantity = ? WHERE id = ?", (food2_quantity - quantity2, 2))
            c.execute("UPDATE restaurant SET quantity = ? WHERE id = ?", (food3_quantity - quantity3, 4))
            conn.commit()
            total_price = quantity1 * food1_details[1] + quantity2 * food2_details[1] + quantity3 * food3_details[1]
            if total_price == 0:
                messagebox.showerror('Error, please purchase an item.')
            else:
                price_label.configure(text=f'price: {total_price}$')
                get_quantity()
                with open('Orders.txt', 'a') as f:
                    f.write(f'name: {customer_entry.get()}\n')
                    f.write(f'total price: {total_price}\n')
                    f.write('----------------\n')
        else:
            messagebox.showerror('Error, please enter your name.')



# this is the function that fetches the food detail from the database
def get_food():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT food_name, price FROM restaurant')
    results = c.fetchall()
    print(results)

    global food1_details
    global food2_details
    global food3_details

    food1_details = results[0]
    food2_details = results[1]
    food3_details = results[2]

    p2_name_label.configure(text="{}\nprice: ${}".format(food1_details[0], food1_details[1]))
    p3_name_label.configure(text="{}\nprice: ${}".format(food2_details[0], food2_details[1]))
    p1_name_label.configure(text="{}\nprice: ${}".format(food3_details[0], food3_details[1]))


    conn.close()



frame1 = customtkinter.CTkFrame(app, bg_color='#000', fg_color='#000', width=1000, height=300)
frame1.place(x=0, y=1)

frame2 = customtkinter.CTkFrame(app, bg_color='#000', fg_color='#0E0F0F', width=700, height=440)
frame2.place(x=0, y=256)

image1 = Image.open('images/food_banner.jpg')
photo1 = ImageTk.PhotoImage(image1)
image1_label = Label(frame1, image=photo1, bg='#000')
image1_label.place(x=-3, y=0)

p1_frame = customtkinter.CTkFrame(frame2, bg_color='#000', fg_color='#333333', corner_radius=20, width=196, height=320)
p1_frame.place(x=20, y=20)
# this is the first product
image2 = Image.open('images/images1.jpg')
photo2 = ImageTk.PhotoImage(image2)
image2_label = Label(p1_frame, image=photo2, bg='#333333')
image2_label.place(x=-1, y=-5)

p1_name_label = customtkinter.CTkLabel(p1_frame, font=font1, text='', text_color='#fff', bg_color='#333333')
p1_name_label.place(x=17, y=200)

p1_quantity = customtkinter.CTkComboBox(p1_frame, font=font1, text_color='#000', fg_color='#fff', dropdown_hover_color='#06911F', button_color='#F67A0D', button_hover_color='#F67A0D', variable=variable1, width=120)
p1_quantity.set(0)
p1_quantity.place(x=40, y=270)

# this is the second product
p2_frame = customtkinter.CTkFrame(frame2, bg_color='#000', fg_color='#333333', corner_radius=20, width=196, height=320)
p2_frame.place(x=250, y=20)

image3 = Image.open('images/jollof-rice (1).png')
photo3 = ImageTk.PhotoImage(image3)
image3_label = Label(p2_frame, image=photo3, bg='#333333')
image3_label.place(x=-1, y=-5)

p2_name_label = customtkinter.CTkLabel(p2_frame, font=font1, text='', text_color='#fff', bg_color='#333333')
p2_name_label.place(x=40, y=200)

p2_quantity = customtkinter.CTkComboBox(p2_frame, font=font1, text_color='#000', fg_color='#fff', dropdown_hover_color='#06911F', button_color='#F67A0D', button_hover_color='#F67A0D', variable=variable2, width=120)
p2_quantity.set(0)
p2_quantity.place(x=40, y=270)

# this is the third product
p3_frame = customtkinter.CTkFrame(frame2, bg_color='#000', fg_color='#333333', corner_radius=20, width=196, height=320)
p3_frame.place(x=480, y=20)

image4 = Image.open('images/chickenrice.jpg')
photo4 = ImageTk.PhotoImage(image4)
image4_label = Label(p3_frame, image=photo4, bg='#333333')
image4_label.place(x=-1, y=-5)

p3_name_label = customtkinter.CTkLabel(p3_frame, font=font1, text='', text_color='#fff', bg_color='#333333')
p3_name_label.place(x=23, y=200)

p3_quantity = customtkinter.CTkComboBox(p3_frame, font=font1, text_color='#000', fg_color='#fff', dropdown_hover_color='#06911F', button_color='#F67A0D', button_hover_color='#F67A0D', variable=variable3, width=120)
p3_quantity.set(0)
p3_quantity.place(x=40, y=270)


# this is the customer label
customer_label = customtkinter.CTkLabel(frame2, font=font1, text='customer:', text_color='#fff', bg_color='#0E0F0F')
customer_label.place(x=50, y=370)

# this is the customer entry field
customer_entry = customtkinter.CTkEntry(frame2, font=font1, text_color='#000', fg_color="#fff", border_color='#fff', width=150)
customer_entry.place(x=160, y=370)

# this is the checkout button

checkout_button = customtkinter.CTkButton(frame2, command=checkout, font=font1, text_color='#fff', text='checkout', fg_color='#410AE3', hover_color='#3303C0', bg_color='#0E0F0F', cursor='hand2', corner_radius=30, width=160, height=50)
checkout_button.place(x=350, y=360)

# price label
price_label = customtkinter.CTkLabel(frame2, font=font1, text='', text_color='#0f0', bg_color='#0E0F0F')
price_label.place(x=550, y=370)


get_food()
get_quantity()


app.mainloop()


