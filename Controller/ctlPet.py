from Classes.clsCat import ClsCat
from Classes.clsDog import ClsDog
from Model.modelCat import ModelCat
from Model.modelDog import ModelDog


class CtlPet:
    def __init__(self, model_dog=None, model_cat=None):
        self.model_dog = model_dog or ModelDog()
        self.model_cat = model_cat or ModelCat()

    def create_pet(self, pet) -> bool:
        if isinstance(pet, ClsDog):
            return self.model_dog.create_pet(pet)
        if isinstance(pet, ClsCat):
            return self.model_cat.create_pet(pet)
        raise TypeError(f"Unsupported pet type: {type(pet).__name__}")

    def search_pet(self, code: str, animal_type: str):
        if animal_type == "Dog":
            return self.model_dog.search_pet(code)
        if animal_type == "Cat":
            return self.model_cat.search_pet(code)
        raise ValueError(f"Unsupported animal type: {animal_type}")

    def edit_pet(self, pet) -> bool:
        if isinstance(pet, ClsDog):
            return self.model_dog.edit_pet(pet)
        if isinstance(pet, ClsCat):
            return self.model_cat.edit_pet(pet)
        raise TypeError(f"Unsupported pet type: {type(pet).__name__}")

    def delete_pet(self, pet) -> bool:
        if isinstance(pet, ClsDog):
            return self.model_dog.delete_pet(pet)
        if isinstance(pet, ClsCat):
            return self.model_cat.delete_pet(pet)
        raise TypeError(f"Unsupported pet type: {type(pet).__name__}")

    def list_pet(self, animal_type: str) -> list:
        if animal_type == "Dog":
            return self.model_dog.list_pet()
        if animal_type == "Cat":
            return self.model_cat.list_pet()
        raise ValueError(f"Unsupported animal type: {animal_type}")

    def list_pet_by_health_status(self) -> list:
        return self.model_cat.list_pet_by_health_status()

    def list_dog_by_health_status(self) -> list:
        return self.model_dog.list_dog_by_health_status()

    def list_cat_by_health_status(self) -> list:
        return self.model_cat.list_cat_by_health_status()
