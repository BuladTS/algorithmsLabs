#ifndef CIMPROVER_IO_FUNCS_H
#define CIMPROVER_IO_FUNCS_H

double **read_csv(char *filepath, int n);

int *read_way(char *filepath, int len);

void save_way(char *filepath, int *way, int len);

void write_matrix(double** matrix, int cols, int rows);

int* ant_alg(double** matrix, int len);

long double** reverse_matrix(double** matrix, int len);

void write_matrix_long(long double** matrix, int cols, int rows);

long double** ones_and_multiply(int len, double value);

void fill_matrix(int** matrix, int cols, int rows, int value);

void fill_array(int* array, int len, int value);

void write_matrix_int(int** matrix, int cols, int rows);

void probability_count(long double* probability_array, long double* reverse_array, long double* pheromone_array, int len, double alpha, double betta);

void write_array_long(long double* array, int len);

long double sum_array_long_double(long double* array, int len);

float get_rand();

void fill_array_double(double* array, int len, int value);

double count_way(double** matrix, int* way, int way_len);

void copy_array_int(int* array, int* copied_array, int len);

void pheromone_disappearance(long double** pheromone_matrix, int size, long double evaporation_coef);

#endif //CIMPROVER_IO_FUNCS_H