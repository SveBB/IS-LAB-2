import random


#   Управление генами
class GeneticCode:
    def __init__(self, dnk: str, goal: str, genes):
        if not dnk:
            self.dnk = ''.join(
                random.choices(genes, k=len(goal))
            )
        else:
            self.dnk = dnk
        self.__goal = goal
        self.__genes = genes

    # Оценка популяции
    def measure(self) -> int:
        score = 0
        for index, gene in enumerate(self.dnk):
            if gene != self.__goal[index]:
                score -= 1
        return score

    #   Мутация
    def mutate(self, number_of_changes: int = 5) -> None:
        new_dnk = list(self.dnk)
        for _ in range(number_of_changes):
            random_index = random.randint(0, len(new_dnk) - 1)
            if self.dnk[random_index] != self.__goal[random_index]:
                new_dnk[random_index] = random.choice(self.__genes)
        self.dnk = "".join(new_dnk)

    #   Кроссинговер
    def crossing_over(self, another_dnk: str) -> str:
        random_slice = random.randint(
            0,
            len(self.dnk) - 1
        )
        return "".join(self.dnk[:random_slice] + another_dnk[random_slice:])


# Управление популяциями
class Pool:
    def __init__(self, pool_size: int, goal: str, genes):
        self.__pool = [GeneticCode('', goal, genes) for _ in range(pool_size)]
        self.__pool_size = pool_size
        self.__genes = genes
        self.__goal = goal

    def get_random(self) -> GeneticCode:
        return self.__pool[random.randint(0, len(self.__pool) - 1)]

    #   Селекция
    def selection(self, cut_off_percentage: float = 0.1) -> None:
        measure_pool = [(item.measure(), item) for item in self.__pool]
        sorted_pool = [item[1] for item in sorted(measure_pool,
                                                  key=lambda x: x[0],
                                                  reverse=True)]
        self.__pool = sorted_pool[:int(round(self.__pool_size * cut_off_percentage))]

        while len(self.__pool) < self.__pool_size:
            new_dnk = self.get_random().crossing_over(self.get_random().dnk)
            new_gene = GeneticCode(
                new_dnk,
                self.__goal,
                self.__genes
            )
            self.__pool.append(new_gene)

    #   Эволюция
    def evolution(self, epoch: int = 1000) -> int:
        for iterations in range(epoch):
            if self.__pool[0].dnk == self.__goal:
                break

            for index, item in enumerate(self.__pool):
                self.__pool[index].mutate()

            self.selection()
            print(self.__pool[0].dnk)

        return iterations


OBJECT = "Мир"

GENES = "".join(
    map(
        lambda x, y: x + y, 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
                            'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    )
)

if __name__ == '__main__':
    #   Размер популяции, слово, набор ген
    breed_pool = Pool(100, OBJECT, GENES)
    steps = breed_pool.evolution()
    print(f"Steps: {steps}")
