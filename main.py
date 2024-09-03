import graph


class World:
    def __init__(self):
        self.gravity = 9.80665 # in m/s^2
        self.timeTickInterval = 0.01 # in seconds


    def get_air_density(self, height):
        # https://en.wikipedia.org/wiki/Density_of_air#Troposphere
        sea_level_pressure = 101325 # in Pa (Pascal)
        sea_level_temperature = 288.15 # in K (Kelvin)
        gravity = self.gravity
        temperature_lapse_rate = 0.0065 # in K/m
        gas_constant = 8.31446 # in J/(mol*K)
        molar_air_mass = 0.0289652 # in kg/mol

        temperature = sea_level_temperature - temperature_lapse_rate * height
        pressure = sea_level_pressure * (1 - ((temperature_lapse_rate * height) / sea_level_temperature))**((gravity * molar_air_mass) / (temperature_lapse_rate * gas_constant))
        density = (pressure * molar_air_mass) / (gas_constant * temperature)

        return density


class FallingObject:

    def __init__(self, world: World):
        self.world = world

        self.height = 0 # in meters
        self.mass = 90 # in kg

        self.drag_coefficient = 1
        self.cross_sectional_area = 1 # in m^2

        self.timeFallen = 0
        self.velocity = 0
        self.acceleration = world.gravity


    def get_gravitational_force(self): # returns force in Newtons (kg*m/s^2)
        return self.mass * self.world.gravity

    def get_air_resistance_force(self): # returns force in Newtons (kg*m/s^2)
        # F = 0.5 * p * C_d * A * v^2
        return 0.5 * self.world.get_air_density(self.height) * self.drag_coefficient * self.cross_sectional_area * self.velocity**2

    def get_final_force(self):
        return self.get_gravitational_force() - (self.get_air_resistance_force())

    def update_velocity(self):
        self.velocity += (self.get_final_force() / self.mass) * self.world.timeTickInterval

    def tick(self):
        self.timeFallen += self.world.timeTickInterval

        self.update_velocity()
        self.height -= self.velocity * self.world.timeTickInterval


w = World()
obj = FallingObject(w)
obj.height = 36529

heightData = ([], [])
velocityData = ([], [])
airResistanceData = ([], [])
finalForceData = ([], [])
airDensityData = ([], [])

while obj.height > 0:
    obj.tick()
    print(f"[{obj.timeFallen}s] {obj.height}m -> {obj.velocity}m/s")

    # Height data
    heightData[0].append(obj.timeFallen)
    heightData[1].append(obj.height)
    # Velocity data
    velocityData[0].append(obj.timeFallen)
    velocityData[1].append(obj.velocity)
    # Air resistance data
    airResistanceData[0].append(obj.timeFallen)
    airResistanceData[1].append(obj.get_air_resistance_force())
    # Final force data
    finalForceData[0].append(obj.timeFallen)
    finalForceData[1].append(obj.get_final_force())
    # Air density data
    airDensityData[0].append(w.get_air_density(obj.height))
    airDensityData[1].append(obj.height)


graph.plot_graph(heightData[0], heightData[1], "Height", "Time (s)", "Height (m)")
graph.plot_graph(velocityData[0], velocityData[1], "Velocity", "Time (s)", "Velocity (m/s)")
graph.plot_graph(airResistanceData[0], airResistanceData[1], "Air Resistance Force", "Time (s)", "Force (N)")
graph.plot_graph(finalForceData[0], finalForceData[1], "Final Force", "Time (s)", "Force (N)")
graph.plot_graph(airDensityData[0], airDensityData[1], "Air Density", "Density (kg/m^3)", "Height (m)")