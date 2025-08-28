class Car:
    def __init__(self, brand, speed):
        self.brand = brand
        self.__speed = speed  # private

    # Getter
    def get_speed(self):
        return self.__speed

    # Setter
    def set_speed(self, value):
        if value < 0:
            print("Speed cannot be negative!")
        else:
            self.__speed = value

car = Car("Toyota", 120)
print(car.get_speed())  # 120

car.set_speed(200)
print(car.get_speed())  # 200

car.set_speed(-50)  # Speed cannot be negative!
