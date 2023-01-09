import sqlite3
import os
from datetime import date


class TrainingHistory:
    def __init__(self):
        """Модуль, позволяющий осуществлять запись и получение данных в / из БД"""
        self.__db_name = os.path.join(os.path.dirname(os.path.abspath(__file__)),'database.db')
        self.__requests = {'get_name_exercise_group': """SELECT [group] FROM name_exercise_group"""
                           ,'get_name_exercise': """SELECT exercise FROM exercises WHERE [group] = ? ORDER BY exercise"""
                           ,'record_training': """INSERT INTO training_history (date, exercise, quantity) VALUES (?, ?, ?)"""      
        }
      
        
    def __connect(self):
        """Приватный метод - подключения к БД"""
        return sqlite3.connect(self.__db_name)
    
    
    def get_name_exercise_group(self) -> list:
        """Возвращает названия групп упражнений (Отжимания/Пресс/Гантели и т.д.)"""
        name_exercise_group = list()
        with self.__connect() as connect:
            cursor = connect.cursor()
            cursor.execute(self.__requests['get_name_exercise_group'])
            for name in cursor.fetchall():
                name_exercise_group.append(str(*name))
        return name_exercise_group
    
    
    def get_name_exercise(self, name_group: str) -> list:
        """Возвращает названия упражнений входящих в группу. В качестве параметра принимает название группы упражнений"""
        name_exercise = list()
        with self.__connect() as connect:
            cursor = connect.cursor()
            cursor.execute(self.__requests['get_name_exercise'], (name_group,))
            for name in cursor.fetchall():
                name_exercise.append(str(*name))
        return name_exercise
    
    
    def record_training(self, exercise: str, count: int) -> str:
        """Записывает в БД информацию о проведенной тренировке (дата, упражнение, кол-во раз)"""
        current_date = date.today()
        try:
            with self.__connect() as connect:
                cursor = connect.cursor()
                cursor.execute(self.__requests['record_training'], (current_date, exercise, count))
                connect.commit()
            return f'Подход записан\n[{current_date}] - [{exercise}] - [{count}]'
        except Exception as exc:
            return f'Произошла ошибка в процессе записи:\n{exc}'
            
   
    

