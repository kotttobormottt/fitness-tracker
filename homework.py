from typing import Dict, List, Type
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:

        INFO_MESSAGE = (
            "Тип тренировки: {training_type}; "
            "Длительность: {duration:.3f} ч.; "
            "Дистанция: {distance:.3f} км; "
            "Ср. скорость: {speed:.3f} км/ч; "
            "Потрачено ккал: {calories:.3f}."
        )
        return INFO_MESSAGE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories,
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOUR: int = 60
    action: int
    duration: float
    weight: float

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIE_MULTIPLIER: int = 18
    CALORIE_SUBSTRACTER: int = 20
    action: int
    duration: float
    weight: float

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = (
            (
                self.CALORIE_MULTIPLIER * self.get_mean_speed()
                - self.CALORIE_SUBSTRACTER
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.HOUR)
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIE_MULTIPLIER_1: float = 0.035
    CALORIE_MULTIPLIER_2: float = 0.029
    action: int
    duration: float
    weight: float
    height: float

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (
            self.CALORIE_MULTIPLIER_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.CALORIE_MULTIPLIER_2
            * self.weight
        ) * (self.duration * self.HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIE_PLUSER: float = 1.1
    CALORIE_MULTIPLIER: float = 2
    LEN_STEP: float = 1.38
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения"""
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных каллорий"""
        spent_calories = (
            (self.get_mean_speed() + self.CALORIE_PLUSER)
            * self.CALORIE_MULTIPLIER
            * self.weight
        )
        return spent_calories


WORKOUT_DICTIONARY: Dict[str, Type[Training]] = {
    "SWM": Swimming,
    "RUN": Running,
    "WLK": SportsWalking,
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in WORKOUT_DICTIONARY:
        raise RuntimeError("Данный вид тренировки отсутствует")
    return WORKOUT_DICTIONARY[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    message_info = info.get_message()
    print(message_info)


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
