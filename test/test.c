#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_SIZE 256
#define FILENAME_SIZE 256

/**********************************************************************/
/* Data structures used in assignment                                 */
/*                                                                    */
/* season list 		the list of seasons for a given sixer player      */
/* player list		the list of all (unique) sixer players            */
/**********************************************************************/

struct season_list {
	char season_name[50];
	int season_salary;
	struct season_list *next;
};

struct player_list {
	char player_name[50];
	int player_no_seasons;
	int player_max_salary_one_season;
	int player_total_salary;
	struct season_list *player_season_list;
	struct player_list *next;
};

/***********************************************/
/* Manipulate the data structure "season_list" */
/***********************************************/

struct season_list *season_list_new(char *season_name, int season_salary)
{
	struct season_list *new;
	
	new = (struct season_list *) malloc (sizeof(struct season_list));
	if (!new) {
		printf("Malloc failed. Exiting.\n");
		exit(-1);
	}
	strcpy(new->season_name, season_name);
	new->season_salary = season_salary;
	new->next = NULL;

	return(new);
}

void season_list_print (struct season_list *list)
{
	struct season_list *p;

	for (p=list; p!=NULL; p=p->next) {
		printf("season name %s with season salary %d \n", 
		p->season_name, 
		p->season_salary);
	}
}

struct season_list *season_list_add(struct season_list *list, 
						char *season_name, int season_salary)
{
	struct season_list *new;

	new = season_list_new(season_name, season_salary);

	if (new) {
		new->next = list;
		return(new);
	}

	return (list);
}


/***********************************************/
/* Manipulate the data structure "player list" */
/***********************************************/


struct player_list *player_list_new (char *player_name, 
									int player_no_seasons,
									int player_max_salary_one_season,
									int player_total_salary, 
									struct season_list *player_season_list)
{
	struct player_list *new;

	new = (struct player_list *) malloc(sizeof(struct player_list));
	if (!new) {
		printf("Malloc failed. Exiting. ");
		exit(-1);
	}
	strcpy(new->player_name, player_name);
	new->player_no_seasons = player_no_seasons;
	new->player_max_salary_one_season  = player_max_salary_one_season;
	new->player_total_salary = player_total_salary;
	new->player_season_list = player_season_list;
	new->next = NULL;
	
	return(new);
}


void player_list_print (struct player_list *list)
{
	struct player_list *p;

	for (p=list; p!=NULL; p=p->next) {
		printf("player name = %s ", p->player_name);
		printf("player no seasons = %d \n", p->player_no_seasons);
		printf("player max salary one season = %d \n", 
			p->player_max_salary_one_season);
		printf("player total salary = %d \n", p->player_total_salary);
		season_list_print(p->player_season_list);
		printf("\n---\n");
	}
}

void player_list_add_season(struct player_list *player_list, 
							struct season_list *new_season)
{
	if (!player_list) return;
	if (!new_season) return;

	new_season->next = player_list->player_season_list;
	player_list->player_season_list = new_season;
	player_list->player_no_seasons += 1;
	if (new_season->season_salary > player_list->player_max_salary_one_season) 
		player_list->player_max_salary_one_season = new_season->season_salary;
	
	player_list->player_total_salary += new_season->season_salary;
}

/******************************************************/
/* Add a player if the player does not exist          */
/* Return a poitner to he player if the player exists */
/******************************************************/

struct player_list *player_list_add_player(
		struct player_list *list, 
		char *name, 
		int no_seasons,
		int max_salary_one_season,
		int salary, 
		char *season)
{
	struct season_list *new_season;
	struct player_list *new_player;
	struct player_list *p;
	struct player_list *found_player;

	new_season = season_list_new(season, salary);

	/* look for the player */

	found_player = NULL;

	for (p=list; p!=NULL; p=p->next) {
		if (strcmp(p->player_name, name) == 0) {
			found_player = p;
			break;
		}
	}
	
	if (!found_player) {
		// printf ("Player %s not found \n", name);

		new_player = player_list_new(
				name, 
				no_seasons, 
				max_salary_one_season, 
				salary, 
				new_season);
		if (new_player) {
			new_player->next = list;
			return(new_player);
		}
	}

	if (found_player) {
		//printf ("Player %s found \n", name);
		
		player_list_add_season(found_player, new_season);
	}

	return (list);
}

/*********************************************/
/* Execute the queries                       */
/*********************************************/


/******************************************************/
/* Query 1                                            */
/* Find the player that played the most seasons       */
/* for the sixers                                     */
/******************************************************/

void find_player_with_most_seasons(struct player_list *list)
{
	struct player_list *p;
	struct player_list *max_player;
	int max;

	/* look for the player */

	max = 0;
	max_player = NULL;

	for (p=list; p!=NULL; p=p->next) {
		if (max < p->player_no_seasons) {
			max = p->player_no_seasons;
			max_player = p;
		}
	}
	
	if (max_player) {
		printf("%s played the most seasons for the sixers: %d seasons\n", 
					max_player->player_name, 
					max_player->player_no_seasons);
	}
}


/******************************************************/
/* Query 2                                            */
/* Find the player that earned the most salary across */
/* all seasons the player played for the sixers       */
/******************************************************/

void find_player_with_max_salary_all_seasons(struct player_list *list)
{
	struct player_list *p;
	struct player_list *max_player;
	int max;

	/* look for the player */

	max = 0;
	max_player = NULL;

	for (p=list; p!=NULL; p=p->next) {
		if (max < p->player_total_salary) {
			max = p->player_total_salary;
			max_player = p;
		}
	}
	
	if (max_player) {
		printf ("%s earned the most money over his career as a sixer: %d\n", 
					max_player->player_name, 
					max_player->player_total_salary);
	}
}

/*************************************************************/
/* Query 3                                                   */
/* Find the player that earned the most salary in one season */
/*************************************************************/

void find_player_with_max_salary_one_season(struct player_list *list)
{
	struct player_list *p;
	struct player_list *max_player;
	int max;

	/* look for the player */

	max = 0;
	max_player = NULL;

	for (p=list; p!=NULL; p=p->next) {
		if (max < p->player_max_salary_one_season) {
			max = p->player_max_salary_one_season;
			max_player = p;
		}
	}
	
	if (max_player) {
		printf ("%s earned the most money in one season as a sixer: %d\n", 
					max_player->player_name, 
					max_player->player_max_salary_one_season);
	}
}

/******************************************************/
/* Main processing: Open the file, read each line,    */
/* tokenize the line and add player to the sixers     */
/* player list                                        */
/******************************************************/

int main(int argc, char *argv[]) {
	FILE *sixers_file;
	char sixers_fn[FILENAME_SIZE];
	char line[LINE_SIZE];
	char *name;
	int salary;
	char *season;
	struct player_list *sixers;
	
	/* Read the command line arguments */

	if (argc == 2) 
		strcpy(sixers_fn, argv[1]);
	else if (argc == 1)
		strcpy(sixers_fn, "sixers.csv");
	else if (argc > 2) {
		printf("Incorrect number of arguments supplied. Exiting. \n");
		exit(-1);
	}

	/* Read the file */
	if ((sixers_file = fopen(sixers_fn, "r")) == NULL) {
		fprintf(stderr, "Error - Unable to open %s. Exiting \n", sixers_fn);
		exit(-1);
	}

	sixers = NULL;
	while (fgets(line, LINE_SIZE, sixers_file) != NULL) {
		name = strtok(line, ",");
		salary = atoi(strtok(NULL, ","));
		season = strtok(NULL, "\n");
		sixers = player_list_add_player(sixers, 
										name, 
										1,       // no of seasons
										salary,  // max one season
										salary,  // total all seasons
										season);
	}

	find_player_with_most_seasons(sixers);
	find_player_with_max_salary_all_seasons(sixers);
	find_player_with_max_salary_one_season(sixers);
}