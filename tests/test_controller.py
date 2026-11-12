import unittest

from Classes.clsCat import ClsCat
from Classes.clsDog import ClsDog
from Controller.ctlPet import CtlPet


class FakeModel:
    def __init__(self, result=True):
        self.result = result
        self.created_pet = None

    def create_pet(self, pet):
        self.created_pet = pet
        return self.result


class CtlPetTests(unittest.TestCase):
    def setUp(self):
        self.dog_model = FakeModel()
        self.cat_model = FakeModel(result=False)
        self.controller = CtlPet(self.dog_model, self.cat_model)

    def test_create_routes_by_pet_class_and_preserves_model_result(self):
        dog = ClsDog()
        cat = ClsCat()

        self.assertTrue(self.controller.create_pet(dog))
        self.assertFalse(self.controller.create_pet(cat))
        self.assertIs(self.dog_model.created_pet, dog)
        self.assertIs(self.cat_model.created_pet, cat)

    def test_unknown_pet_type_is_rejected(self):
        with self.assertRaises(TypeError):
            self.controller.create_pet(object())


if __name__ == "__main__":
    unittest.main()
