import csv
from external_sort import copy_csv


def main():
    key = "sort"

    copy_csv("file.csv")
    # ls = [1, 4, 4, 2, 1, 5, 3, 1, 3]
    # ptr = open("file.csv", "w", newline="", encoding="utf-8")
    # writer = csv.DictWriter(ptr, fieldnames=[key])
    # writer.writeheader()
    # for i in ls:
    #     writer.writerow({key: int(i)})
    # ptr.close()
    #
    # exit_file = []
    # ptr = open("file.csv", "r", encoding="utf-8")
    # reader = csv.DictReader(ptr)
    # for i in reader:
    #     print(i[key], type(i[key]))
    # # for _ in range(len(ls)):
    # #     exit_file.append(int(next(reader)[key]))
    # #     print(exit_file[-1])
    #
    # ptr.close()


if __name__ == '__main__':
    main()
