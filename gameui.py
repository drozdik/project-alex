from cgitb import text
import tkinter
from tkinter import *


from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText

from controller import Controller
from model import Model


class Screen:

    def __init__(self, hero_attack, use_heal, game_state, game_restart, use_precision_strike, use_aoe_strike, use_combo_strike, controller: Controller):
        # state
        self.game_state = game_state
        # hook functions
        self.hero_attack = hero_attack
        self.use_heal = use_heal
        self.game_restart = game_restart
        self.use_precision_strike = use_precision_strike
        self.use_aoe_strike = use_aoe_strike
        self.use_combo_strike = use_combo_strike
        self.controller = controller
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
        self.skeleton_lich_image = ImageTk.PhotoImage(Image.open("images/skeleton-lich.png"))

        self.draw_images_and_buttons()
        self.draw_status_panels()
        self.draw_health_panels()
        self.draw_log_panel()
        self.events = []

    def display(self):
        self.dispatch_events()
        self.root.mainloop()

    def print_stuff(self):
        print("Event")

    def dispatch_events(self):
        if(len(self.events) > 0):
            cmd = self.events.pop()
            cmd.execute()
            self.root.after(1000, self.dispatch_events)
        else:
            self.root.after(1000, self.dispatch_events)



    def draw_log_panel(self):
        log_content = ""
        for log in self.game_state.get("game_log"):
            log_content += log + "\n"
        self.log_panel = ScrolledText(self.frame, width=80,  height=15)
        self.log_panel.grid(row=8, column=0, columnspan=3)
        self.log_panel.insert(INSERT, log_content)
        self.log_panel.configure(state ='disabled')
        self.log_panel.see("end")

    def on_hero_attack(self):
        self.remember_all_hp_and_pack()
        self.hero_attack()  # calls action from the Game
        self.update_components()

    def on_hero_heal(self):
        self.remember_all_hp_and_pack()
        self.controller.use_heal()

    def on_hero_precision_strike(self):
        self.remember_all_hp_and_pack()
        self.use_precision_strike()
        self.update_components()

    def on_hero_aoe_strike(self):
        self.remember_all_hp_and_pack()
        self.use_aoe_strike()
        self.update_components()

    def on_hero_combo_strike(self):
        self.remember_all_hp_and_pack()
        self.use_combo_strike()
        self.update_components()

    def quit(self):
        self.root.destroy()

    def on_restart(self):
        self.game_restart()
        # destroy frame, which contains Game Over and buttons
        self.frame.destroy()
        # create fresh frame
        self.frame = tkinter.Frame(self.root)
        self.frame.grid()
        # redraw dynamic elements (log, health)
        self.redraw_game_components()

    def redraw_game_components(self):
        self.draw_images_and_buttons()
        self.draw_health_panels()
        self.log_panel = None
        self.draw_log_panel()
        self.draw_status_panels()

    # images and buttons
    def draw_images_and_buttons(self):
        self.knight_image_label = Label(self.frame, image=self.knight_image)
        self.knight_image_label.grid(row=1, column=0, columnspan=1)
        monster1_image = self.get_monster_image(self.game_state["active_monster_pack"][0])
        self.monster1_image_label = Label(self.frame, image=monster1_image)
        self.monster1_image_label.grid(row=1, column=1, columnspan=1)

        monster2_image = self.get_monster_image(self.game_state["active_monster_pack"][1])
        self.monster2_image_label = Label(self.frame, image=monster2_image)
        self.monster2_image_label.grid(row=1, column=2, columnspan=1)

        hero_attack_button = Button(self.frame, text="Attack and finish turn", command=self.on_hero_attack)
        hero_attack_button.grid(row=3, column=0, columnspan=1)

        self.hero_heal_button = Button(self.frame, text="Heal", command=self.on_hero_heal)
        self.hero_heal_button.grid(row=4, column=0, columnspan=1)

        hero_precision_strike_button = Button(self.frame, text="Precision Strike", command=self.on_hero_precision_strike)
        hero_precision_strike_button.grid(row=5, column=0, columnspan=1)

        hero_aoe_strike_button = Button(self.frame, text="AOE Strike", command=self.on_hero_aoe_strike)
        hero_aoe_strike_button.grid(row=6, column=0, columnspan=1)

        hero_aoe_strike_button = Button(self.frame, text="Combo Strike", command=self.on_hero_combo_strike)
        hero_aoe_strike_button.grid(row=7, column=0, columnspan=1)

    def draw_status_panels(self):
        self.hero_status = Label(self.frame, text="", font="Arial 14 bold", fg='red')
        self.hero_status.grid(row=0, column=0, columnspan=1)
        self.monster1_status = Label(self.frame, text="", font="Arial 14 bold", fg='red')
        self.monster1_status.grid(row=0, column=1, columnspan=1)
        self.monster2_status = Label(self.frame, text="", font="Arial 14 bold", fg='red')
        self.monster2_status.grid(row=0, column=2, columnspan=1)

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
    
    def get_hero_text(self):
        hp_row = f"Health: {self.game_state.get('hero_hp')}/{self.game_state.get('hero_max_hp')}"
        class_row = f"Class: Knight"
        armor_row = f"Armor: {self.game_state.get('hero_armor')}"
        damage_row = f"Damage: { self.game_state.get('hero_min_damage')} - {self.game_state.get('hero_max_damage')}"
        healing_potions_row = f"Potions: {self.game_state.get('healing_potions')}"
        text = f"{class_row}\n{hp_row}\n{armor_row}\n{damage_row}\n{healing_potions_row}"
        return text
    
    def get_monster_image(self, monster):
        monster_image = self.skeleton_image
        if monster["class"] == "Skeleton-mage":
            monster_image = self.skeleton_mage_image
        elif monster["class"] == "Skeleton-Lich":
            monster_image = self.skeleton_lich_image
        return monster_image

    def get_monster_text(self,monster):
        monster_name = monster["class"]
        monster_hp = monster["hp"]
        monster_armor = monster["armor"]
        monster_min_damage = monster["min_damage"]
        monster_max_damage = monster["max_damage"]
        monster_damage = f"Damage:{monster_min_damage} - {monster_max_damage}"

        text = f"Class:{monster_name}\nHealtn:{monster_hp}\nArmor:{monster_armor}\n{monster_damage}"
        return text
    
    def show_hero_hp_status(self, model):
        self.hero_status.config(text=f"{'%+d' % (model.get_hero_hp_diff())}")


    def on_model_update(self, model:Model):
        # hero hp changed
        self.hero_status.config(text="")
        if model.hero_hp_changed():
            #self.hero_status.config(text=f"{'%+d' % (model.get_hero_hp_diff())}")
            self.events.append(MyCommand(self.show_hero_hp_status, model))
            # time.sleep - bad idea
        #self.root.after(500, self.update_components) # doesn't work either

    def update_components(self):
        if self.game_state.get('healing_potions') == 0:
            self.hero_heal_button.config(state='disabled')
        if self.game_state.get("hero_dead"):
            self.destroy_frame()
            self.draw_game_over_components("Hero is dead. Game Over.")
            return
        elif self.game_state.get("monsters_dead"):
            self.destroy_frame()
            self.draw_game_over_components("Monsters are dead. Game Over.")
            return

        # forget health panels
        # update hero panel
        hero_text = self.get_hero_text()
        self.hero_health_label.config(text=hero_text,font=("Arial", 14))
        # update monster1 panel
        monster1 = self.game_state['active_monster_pack'][0] # it's dictionary now
        monster1_text = self.get_monster_text(monster1)
        self.monster_1_health_label.config(text= monster1_text,font=("Arial", 14))
        # update monster2 panel
        monster2 = self.game_state['active_monster_pack'][1] # it's dictionary now
        monster2_text = self.get_monster_text(monster2)
        self.monster_2_health_label.config(text= monster2_text,font=("Arial", 14))
                                        
        # update log panel
        log_content = ""
        for log in self.game_state.get("game_log"):
            log_content += log + "\n"
        self.log_panel.configure(state ='normal')
        self.log_panel.insert(INSERT, log_content)
        self.log_panel.configure(state ='disabled')
        self.log_panel.see("end")
        # update monster images
        monster1_image = self.get_monster_image(self.game_state["active_monster_pack"][0])
        self.monster1_image_label.config(image=monster1_image)

        monster2_image = self.get_monster_image(self.game_state["active_monster_pack"][1])
        self.monster2_image_label.config(image=monster2_image)
        self.update_status_labels()

    def update_status_labels(self):
        self.monster1_status.config(text="")
        self.monster2_status.config(text="")
        if(self.monster_pack != self.get_active_monster_pack()):
            # pack changed, leave empty statuses
            return

        if self.monster1_hp != self.get_monster1_hp():
            self.monster1_status.config(text=f"{self.get_monster1_hp() - self.monster1_hp}")
        if self.monster2_hp != self.get_monster2_hp():
            self.monster2_status.config(text=f"{self.get_monster2_hp() - self.monster2_hp}")

        
    def draw_health_panels(self):
        self.hero_health_label = Label(self.frame,
                                text = self.get_hero_text(),
                                font=("Arial", 14))
        self.hero_health_label.grid(row=2, column=0)

        monster1 = self.game_state['active_monster_pack'][0] # it's dictionary now
        self.monster_1_health_label = Label(self.frame, text=self.get_monster_text(monster1),font=("Arial", 14))
        self.monster_1_health_label.grid(row=2, column=1)

        monster2 = self.game_state['active_monster_pack'][1] # it's dictionary now
        self.monster_2_health_label = Label(self.frame, text=self.get_monster_text(monster2),font=("Arial", 14))
        self.monster_2_health_label.grid(row=2, column=2)

    def remember_all_hp_and_pack(self):
        self.hero_hp = self.get_hero_hp()
        self.monster1_hp = self.get_monster1_hp()
        self.monster2_hp = self.get_monster2_hp()
        self.monster_pack = self.get_active_monster_pack()

    def get_hero_hp(self):
        return self.game_state.get('hero_hp')

    def get_monster1_hp(self):
        return self.game_state["active_monster_pack"][0]["hp"]

    def get_monster2_hp(self):
        return self.game_state["active_monster_pack"][1]["hp"]

    def get_active_monster_pack(self):
        return self.game_state["active_monster_pack"]


class MyCommand:
    def __init__(self, func, model:Model) -> None:
        self.func=func
        self.model=model

    def execute(self):
        self.func(self.model)