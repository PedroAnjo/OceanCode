class NavigationController:
    def __init__(self, state):
        self.state = state
        self.active = "start"

    def back(self):
        self.active = {"missions": "start", "levels": "missions", "game": "levels"}.get(self.active, "start")

    def mission(self, number):
        mission = next((m for m in self.state.missions if m.number == number), None)
        if mission and mission.available:
            self.state.selected_mission = mission
            self.state.selected_level = None
            self.active = "levels"

    def level(self, number):
        mission = self.state.selected_mission
        level = next((l for l in mission.levels if l.number == number), None) if mission else None
        if level and level.playable:
            self.state.selected_level = level
            self.state.commands.clear()
            self.state.message = "Adicione comandos para planejar sua rota."
            self.active = "game"
