#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <float.h>
#include "file_funcs.h"


const float RAND_MAX_F = RAND_MAX;


double **read_csv(char *filepath, int n) {
    double **matrix = (double **) malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        matrix[i] = (double *) malloc(n * sizeof(double));
    }

    FILE *file = fopen(filepath, "r");
    if (file == NULL) {
        printf("Не удалось открыть файл\n");
        return NULL;
    }



    char buffer[79150];
    int row = 0;
    while (fgets(buffer, sizeof(buffer), file)) {

        int col = 0;
        char *token = strtok(buffer, "|");
        while (token != NULL && col < n) {
            sscanf(token, "%lf", &matrix[row][col]);
            token = strtok(NULL, "|");
            col++;
        }
        printf("Read row %d\n", row);
        row++;

    }
    fclose(file);
    return matrix;
}

int *read_way(char *filepath, int len) {
    int *way = malloc(len * sizeof(int));
    FILE *file = fopen(filepath, "r");
    if (!file) {
        printf("Не удалось открыть файл\n");
        return NULL;
    }

    int num;
    for (int i = 0; i < len; ++i) {
        fscanf(file, "%d", &num);
        way[i] = num;

    }
    fclose(file);
    return way;
}

void save_way(char *filepath, int *way, int len) {
    FILE *file = fopen(filepath, "w");
    for (int i = 0; i < len; ++i) {
        fprintf(file, "%d\n", way[i]);
    }
    fclose(file);
}

void write_matrix(double** matrix, int cols, int rows) {
    for (int i = 0; i < cols; ++i) {
        for (int j = 0; j < rows; ++j)
            printf("%10f ", matrix[i][j]);
        printf("\n");
    }

}

void write_matrix_long(long double** matrix, int cols, int rows) {
    for (int i = 0; i < cols; ++i) {
        for (int j = 0; j < rows; ++j)
            printf("%10LF ", matrix[i][j]);
        printf("\n");
    }

}

void write_matrix_int(int** matrix, int cols, int rows) {
    for (int i = 0; i < cols; ++i) {
        for (int j = 0; j < rows; ++j)
            printf("%d ", matrix[i][j]);
        printf("\n");
    }
}

void write_array_long(long double* array, int len) {
    for (int i = 0; i < len; ++i) {
        printf("%LF\n", array[i]);
    }
}


int* ant_alg(double** matrix, int len) {
    int* best_way;
    double best_dist = DBL_MAX;
    int start_city;

    long double sum_probability;
    int city_to;
    int city_from;
    unsigned long long rand_flag = 1;

    int ages = 80;
    int ants = 100;
    int start_index = 0;
    double ph = 0.00001;
    double alpha = 2;
    double betta = 0.5;
    long double pheromone = 0.5;

    int cities = len;

    best_way = (int*) calloc(cities, sizeof (int ));

    long double** reversed_matrix = reverse_matrix(matrix, cities);
    long double** pheromone_matrix = ones_and_multiply(cities, ph);

    int** ant_routes = (int**) calloc(ants, sizeof (int*));
    for (int i = 0; i < ants; ++i)
        ant_routes[i] = (int*) calloc(cities, sizeof (int));

    double * ant_dists = (double*) calloc(ants, sizeof (double));

    long double* probability = calloc(cities, sizeof (long double));

    for (int age = 0; age < ages; ++age) {
        fill_matrix(ant_routes, ants, cities, 0);
        fill_array_double(ant_dists, ants, 0);

        for (int k = 0; k < ants; ++k) {
            if (k == 0)
                ant_routes[k][0] = start_index;
            else
                ant_routes[k][0] = ant_routes[k - 1][cities - 1];

            for (int s = 1; s < cities; ++s) {
                start_city = ant_routes[k][s - 1];

                probability_count(probability, reversed_matrix[start_city], pheromone_matrix[start_city], cities, alpha, betta);

                for (int i = 0; i < s; ++i)
                    probability[ant_routes[k][i]] = 0;

                sum_probability = sum_array_long_double(probability, cities);

                for (int i = 0; i < cities; ++i)
                    probability[i] = probability[i] / sum_probability;

                int is_chosen = 0;
                while (is_chosen == 0) {
                    srand(rand_flag);
                    rand_flag += s * 31 + 5;
                    rand_flag += k * 7;
                    rand_flag *= 29;
                    float rand = get_rand();
                    for (int i = 0; i < cities; ++i)
                        if (probability[i] > rand) {
                            ant_routes[k][s] = i;
                            is_chosen = 1;
                        }
                }
                if (rand_flag > 10000000000000000)
                    rand_flag = 1;
            }

            ant_dists[k] = count_way(matrix, ant_routes[k], cities);

            if (ant_dists[k] < best_dist) {
                best_dist = ant_dists[k];
                copy_array_int(best_way, ant_routes[k], cities);
            }

            printf("Муравей %d/%d прошел все города, поколение %d\n", k + 1, ants, age + 1);
        }

        for (int k = 0; k < ants; ++k) {
            city_to = ant_routes[k][0];
            city_from = ant_routes[k][cities - 1];

            pheromone_matrix[city_from][city_to] += pheromone;
            pheromone_matrix[city_to][city_from] += pheromone;
            for (int s = 1; s < cities; ++s) {
                city_to = ant_routes[k][s];
                city_from = ant_routes[k][s - 1];

                pheromone_matrix[city_from][city_to] += pheromone;
                pheromone_matrix[city_to][city_from] += pheromone;
            }
        }

        pheromone_disappearance(pheromone_matrix, cities, pheromone);

        printf("Поколение %d/%d прошло\n", age + 1, ages);
    }

    for (int i = 0; i < cities; ++i) {
        free(reversed_matrix[i]);
        free(pheromone_matrix[i]);
    }
    free(reversed_matrix);
    free(pheromone_matrix);

    for (int i = 0; i < ants; ++i) {
        free(ant_routes[i]);
    }
    free(ant_routes);
    free(ant_dists);

    printf("Лучшее растояние %F\n", best_dist);

    return best_way;
}

void pheromone_disappearance(long double** pheromone_matrix, int size, long double evaporation_coef) {
    for (int i = 0; i < size; ++i)
        for (int j = 0; j < size; ++j)
            pheromone_matrix[i][j] *= (1 - evaporation_coef);
}

void copy_array_int(int* array, int* copied_array, int len) {
    for (int i = 0; i < len; ++i)
        array[i] = copied_array[i];
}

double count_way(double** matrix, int* way, int way_len) {
    double distance = 0;
    distance += matrix[way[0]][way[way_len - 1]];
    for (int i = 0; i < way_len - 1; ++i)
        distance += matrix[way[i]][way[i + 1]];

    return distance;
}

float get_rand() {
    return rand() / RAND_MAX_F;
}

long double sum_array_long_double(long double* array, int len) {
    long double sum = 0;
    for (int i = 0; i < len; ++i)
        sum += array[i];
    return sum;
}


void fill_matrix(int** matrix, int cols, int rows, int value) {
    for (int i = 0; i < cols; ++i)
        for (int j = 0; j < rows; ++j) {
            matrix[i][j] = value;
        }
}


void probability_count(long double* probability_array, long double* reverse_array, long double* pheromone_array, int len, double alpha, double betta) {
    long double* rev_array_powered = calloc(len, sizeof (long double));
    long double* pheromone_array_powered = calloc(len, sizeof (long double));
    for (int i = 0; i < len; ++i) {
        rev_array_powered[i] = powl(reverse_array[i], betta);
        pheromone_array_powered[i] = powl(pheromone_array[i], alpha);
    }

    for (int i = 0; i < len; ++i) {
        probability_array[i] = rev_array_powered[i] * pheromone_array_powered[i];
    }

    free(rev_array_powered);
    free(pheromone_array_powered);

}

void fill_array_double(double* array, int len, int value) {
    for (int i = 0; i < len; ++i) {
        array[i] = value;
    }
}

void fill_array(int* array, int len, int value) {
    for (int i = 0; i < len; ++i) {
        array[i] = value;
    }
}

long double** reverse_matrix(double** matrix, int len) {
    long double** reverse_matrix = calloc(len, sizeof (long double*));
    for (int i = 0; i < len; ++i) {
        reverse_matrix[i] = calloc(len, sizeof(long double));
    }

    for (int i = 0; i < len - 1; ++i)
        for (int j = i + 1; j < len; ++j) {
            reverse_matrix[i][j] = 1 / matrix[i][j];
            reverse_matrix[j][i] = 1 / matrix[i][j];
        }
    return reverse_matrix;
}

long double** ones_and_multiply(int len, double value) {
    long double** matrix = calloc(len, sizeof (long double*));
    for (int i = 0; i < len; ++i) {
        matrix[i] = calloc(len, sizeof(long double));
    }

    for (int i = 0; i < len; ++i)
        for (int j = 0; j < len; ++j)
            matrix[i][j] = value;

    return matrix;

}