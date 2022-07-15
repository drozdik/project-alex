import tkinter
from tkinter import *

from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText


class Screen:

    def __init__(self, hero_attack, use_heal, game_state, game_restart):
        # state
        self.game_state = game_state
        # hook functions
        self.hero_attack = hero_attack
        self.use_heal = use_heal
        self.game_restart = game_restart
        # init root with title
        self.root = Tk()
        self.root.title("Diablo dnd edition")
        # init frame
        self.frame = tkinter.Frame(self.root)
        self.frame.grid()
        # create images
        self.knight_image = ImageTk.PhotoImage(Image.open("images/knight.png"))
        self.skeleton_image = ImageTk.PhotoImage(Image.open("images/skeleton.png"))
        self.skeleton_mage_image = ImageTk.PhotoImage(Image.open("images/skeleton-mage.png"))

        self.draw_images_and_buttons()
        self.draw_health_panels()
        self.draw_log_panel()

        # start UI
        self.root.mainloop()


    def draw_log_panel(self):
        log_content = ""
        for log in self.game_state.get("game_log"):
            log_content += log + "\n"

        self.log_panel = ScrolledText(self.frame, width=50,  height=10)
        self.log_panel.grid(row=4, column=0, columnspan=3)
        self.log_panel.insert(INSERT, log_content)
        self.log_panel.configure(state ='disabled')
        self.log_panel.see("end")

    def on_hero_attack(self):
        self.hero_attack()  # calls action from the Game
        self.redraw_panels()

    def on_hero_heal(self):
        self.use_heal()
        self.redraw_panels()

    def quit(self):
        self.root.destroy()

    def on_restart(self):
        print("on restart called")
        self.game_restart()
        # destroy frame, which contains Game Over and buttons
        print("destroying frame with Game Over")
        self.frame.destroy()
        # create fresh frame
        self.frame = tkinter.Frame(self.root)
        self.frame.grid()
        # redraw dynamic elements (log, health)
        self.redraw_panels(True)

    # images and buttons
    def draw_images_and_buttons(self):
        knight_image_label = Label(self.frame, image=self.knight_image)
        knight_image_label.grid(row=0, column=0, columnspan=1)

        monster1_image = self.skeleton_image
        if self.game_state["active_monster_pack"][0]["name"] == "Skeleton-mage":
            print("monster is mage")
            monster1_image = self.skeleton_mage_image
        monster1_image_label = Label(self.frame, image=monster1_image)
        monster1_image_label.grid(row=0, column=1, columnspan=1)

        monster2_image = self.skeleton_image
        if self.game_state["active_monster_pack"][1]["name"] == "Skeleton-mage":
            print("monster is mage")
            monster2_image = self.skeleton_mage_image
        monster2_image_label = Label(self.frame, image=monster2_image)
        monster2_image_label.grid(row=0, column=2, columnspan=1)

        hero_attack_button = Button(self.frame, text="Attack and finish turn", command=self.on_hero_attack)
        hero_attack_button.grid(row=2, column=0, columnspan=1)

        hero_heal_button = Button(self.frame, text="Heal", command=self.on_hero_heal)
        hero_heal_button.grid(row=3, column=0, columnspan=1)

    def draw_game_over_components(self, text="Game Over."):
        l_game_over = Label(self.frame, text=text)
        l_game_over.grid(row=0, column=0, columnspan=1)
        b_quite = Button(self.frame, text="Quit", command=self.quit)
        b_quite.grid(row=1, column=0, columnspan=1)
        b_restart = Button(self.frame, text="Restart", command=self.on_restart)
        b_restart.grid(row=1, column=1, columnspan=1)

    def destroy_frame(self):
        self.frame.destroy()
        self.frame = tkinter.Frame(self.root)
        self.frame.grid()

    def redraw_panels(self, with_static=False):
        if with_static:
            self.draw_images_and_buttons()
        if self.game_state.get("hero_dead"):
            self.destroy_frame()
            self.draw_game_over_components("Hero is dead. Game Over.")
            return
        elif self.game_state.get("monsters_dead"):
            self.destroy_frame()
            self.draw_game_over_components("Monsters are dead. Game Over.")
            return

        # forget health panels
        self.hero_health_label.grid_forget()
        self.monster_1_health_label.grid_forget()
        self.monster_2_health_label.grid_forget()
        self.draw_health_panels()

        self.log_panel.grid_forget()
        self.draw_log_panel()

    def draw_health_panels(self):
        self.hero_health_label = Label(self.frame,
                                text=f"Class: Knight\nHealth: {self.game_state.get('hero_hp')}/{self.game_state.get('hero_max_hp')}")
        self.hero_health_label.grid(row=1, column=0)

        monster1 = self.game_state['active_monster_pack'][0] # it's dictionary now
        monster1_name = monster1["name"]
        monster1_hp = monster1["hp"]
        self.monster_1_health_label = Label(self.frame, text=f"{monster1_name} health: {monster1_hp}")
        self.monster_1_health_label.grid(row=1, column=1)

        monster2 = self.game_state['active_monster_pack'][1] # it's dictionary now
        monster2_name = monster2["name"]
        monster2_hp = monster2["hp"]
        self.monster_2_health_label = Label(self.frame, text=f"{monster2_name} health: {monster2_hp}")
        self.monster_2_health_label.grid(row=1, column=2)
