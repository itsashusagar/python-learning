# Class banayi
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def show_details(self):
        print(f"Car: {self.brand} {self.model}")

# Object banaya
car1 = Car("Toyota", "Fortuner")
car2 = Car("Tesla", "Model X")

car1.show_details()
car2.show_details()
