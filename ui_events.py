import threading
from queue import Queue


class UiEventsListener:

    def __init__(self, queue, game):
        self.queue = queue
        self.game = game

    def watch_queue(self):
        while True:
            if not self.queue.empty():
                event = self.queue.get()
                print(f"picked event {event}")
                if event == "hero_attack":
                    hero_attack_inside()
                elif event == "hero_heal":
                    use_heal_inside()
                elif event == "precision_strike":
                    use_precision_strike_inside()
                elif event == "aoe_strike":
                    use_aoe_strike_inside()
                elif event == "combo_strike":
                    use_combo_strike_inside()
                elif event == "block":
                    use_block_inside()
                elif event == "restart":
                    screen.show_on_restart()

    def start_listening(self):
        queue_watcher = threading.Thread(target=self.watch_queue,
                                         args=[self.queue])
        queue_watcher.setDaemon(True)
        queue_watcher.start()
