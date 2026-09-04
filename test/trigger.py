from ursina import Ursina, Entity, color, held_keys, time, Func
from ursina.trigger import Trigger

if __name__ == '__main__':
    app = Ursina()
    player = Entity(model="cube", color=color.azure, scale=0.05)
    
    def update():
        player.x += held_keys["d"] * time.dt * 2
        player.x -= held_keys["a"] * time.dt * 2

    trigger = Trigger(trigger_targets=(player,), x=1, model="sphere", color=color.hsv(0,1,1,0.5))
    trigger.on_trigger_enter = Func(print, "enter")
    trigger.on_trigger_exit = Func(print, "exit")
    trigger.on_trigger_stay = Func(print, "stay")

    app.run()