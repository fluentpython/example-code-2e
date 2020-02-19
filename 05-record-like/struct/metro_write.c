#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define LEN 3

struct MetroArea {
    int year;
    char name[12];
    char country[2];
    float population;
};

int main(int argc, char* argv[]) {
    struct MetroArea metro[LEN];
    int rank;

    metro[0].year = 2018;
    strcpy(metro[0].name, "Tokyo");
    metro[0].country[0] = 'J';
    metro[0].country[1] = 'P';
    metro[0].population = 43868229.0;

    metro[1].year = 2015;
    strcpy(metro[1].name, "Shanghai");
    metro[1].country[0] = 'C';
    metro[1].country[1] = 'N';
    metro[1].population = 38700000.0;

    metro[2].year = 2015;
    strcpy(metro[2].name, "Jakarta");
    metro[2].country[0] = 'I';
    metro[2].country[1] = 'D';
    metro[2].population = 31689592.0;

    FILE* data;
    if ( (data = fopen("metro_areas.bin", "wb")) == NULL ) {
        printf("Error opening file\n");
        return 1;   
    }

    fwrite(metro, sizeof(struct MetroArea), LEN, data);
    fclose(data);

    return 0;
}
