import csv
import sys
import os

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people (for small dataset)
    try:
        with open(os.path.join(fr"{directory}", "people.csv"), encoding="utf-8") as f:
        #with open(fr"{directory}\people.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                people[row["id"]] = {
                    "name": row["name"],
                    "birth": row["birth"],
                    "movies": set()
                }
                if row["name"].lower() not in names:
                    names[row["name"].lower()] = {row["id"]}
                else:
                    names[row["name"].lower()].add(row["id"])
    
    # Load people1 and people2 (for large datasets)
    except:
        with open(os.path.join(fr"{directory}", "people1.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                people[row["id"]] = {
                    "name": row["name"],
                    "birth": row["birth"],
                    "movies": set()
                }
                if row["name"].lower() not in names:
                    names[row["name"].lower()] = {row["id"]}
                else:
                    names[row["name"].lower()].add(row["id"])
                    
        # Load people2
        with open(os.path.join(fr"{directory}", "people2.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                people[row["id"]] = {
                    "name": row["name"],
                    "birth": row["birth"],
                    "movies": set()
                }
                if row["name"].lower() not in names:
                    names[row["name"].lower()] = {row["id"]}
                else:
                    names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #take care of bad input
    if(source == target):
        return []
    
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    
    #used to store states (actors) we've already explored
    explored = set()
    
    while True:
        #we've exhausted all connections between actors and
        #no connection found
        if frontier.empty():
            return None

        node = frontier.remove()
        #is this next node what we are looking for?
        #
        # Note: code below to check if we reached our goal is from the lecture.
        #       as suggested by the homework hint, we improve the efficiency of
        #       the search by checking a node before adding it to the frontier.
        #
        #if(node.state == target):
        #    #yes it is, let's retrace our steps through the graph
        #    #and record what (movie, people) pairs brought us here
        #    return get_path(node)
        
        #if we're here, we haven't reached our 'target' state,
        #so let's add this node to the list of explored and move on
        explored.add(node.state)
        
        #what are the other people(nodes) connected to my current actor (node)?
        #let's get those connections and expand our graph(frontier)
        for movie, person in neighbors_for_person(node.state):

            if not frontier.contains_state(person) and person not in explored:
                child = Node(state=person, parent=node, action=movie)
                
                #as we add more people to our graph, let's first check if
                #we come across our goal
                if(child.state == target):
                    return get_path(child)

                frontier.add(child)


def get_path(node):
    """
    Returns the path taken so far to reach
    current state(node). path is represented in (action, state) pairs
    """
    path = []
    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent
        
    path.reverse()
    return path
    

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()

    
