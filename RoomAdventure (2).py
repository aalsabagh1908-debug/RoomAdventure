/**********************************************************************
 * Name: Ahmed AlSabagh
 * Date: 11/8/2025
 * Description: Room Adventure Game (4 rooms + 2 added features)
 * Features added:
 *  1. Added Room 3 (Kitchen) and Room 4 (Basement)
 *  2. Added "use" command to let player use key/torch
 *  3. Added "drop" command to remove items from inventory
 *********************************************************************/

import java.util.ArrayList;
import java.util.Scanner;

//--------------------------------------------------------------------
// Room class blueprint
//--------------------------------------------------------------------
class Room {
    private String name;
    private ArrayList<String> exits;
    private ArrayList<Room> exitLocations;
    private ArrayList<String> items;
    private ArrayList<String> itemDescriptions;
    private ArrayList<String> grabbables;

    public Room(String name) {
        this.name = name;
        exits = new ArrayList<>();
        exitLocations = new ArrayList<>();
        items = new ArrayList<>();
        itemDescriptions = new ArrayList<>();
        grabbables = new ArrayList<>();
    }

    public String getName() { return name; }
    public ArrayList<String> getExits() { return exits; }
    public ArrayList<Room> getExitLocations() { return exitLocations; }
    public ArrayList<String> getItems() { return items; }
    public ArrayList<String> getItemDescriptions() { return itemDescriptions; }
    public ArrayList<String> getGrabbables() { return grabbables; }

    public void addExit(String exit, Room room) {
        exits.add(exit);
        exitLocations.add(room);
    }

    public void addItem(String item, String desc) {
        items.add(item);
        itemDescriptions.add(desc);
    }

    public void addGrabbable(String item) {
        grabbables.add(item);
    }

    public void delGrabbable(String item) {
        grabbables.remove(item);
    }

    @Override
    public String toString() {
        StringBuilder s = new StringBuilder();
        s.append("\nYou are in ").append(name).append(".\n");
        s.append("You see: ");
        for (String item : items) s.append(item).append("  ");
        s.append("\nGrabbables: ");
        for (String g : grabbables) s.append(g).append("  ");
        s.append("\nExits: ");
        for (String exit : exits) s.append(exit).append("  ");
        s.append("\n");
        return s.toString();
    }
}

//--------------------------------------------------------------------
// Main Game class
//--------------------------------------------------------------------
public class RoomAdventure {
    private static Room currentRoom;
    private static ArrayList<String> inventory = new ArrayList<>();

    //----------------------------------------------------------------
    // Create the rooms and set up connections
    //----------------------------------------------------------------
    public static void createRooms() {
        Room room1 = new Room("Living Room");
        Room room2 = new Room("Library");
        Room room3 = new Room("Kitchen");
        Room room4 = new Room("Basement");

        // Room 1 connections and items
        room1.addExit("east", room2);
        room1.addExit("south", room3);
        room1.addItem("chair", "A small wooden chair.");
        room1.addItem("table", "A round table with a shiny key on top.");
        room1.addGrabbable("key");

        // Room 2 connections and items
        room2.addExit("west", room1);
        room2.addExit("south", room4);
        room2.addItem("rug", "A dusty old rug.");
        room2.addItem("fireplace", "A cold fireplace full of ashes.");

        // Room 3 connections and items
        room3.addExit("north", room1);
        room3.addExit("east", room4);
        room3.addItem("fridge", "It hums quietly. There’s a torch inside.");
        room3.addGrabbable("torch");

        // Room 4 connections and items
        room4.addExit("north", room2);
        room4.addExit("west", room3);
        room4.addItem("chest", "A locked chest sits in the corner.");
        room4.addGrabbable("gold coin");

        currentRoom = room1;
    }

    //----------------------------------------------------------------
    // Main gameplay loop
    //----------------------------------------------------------------
    public static void main(String[] args) {
        createRooms();
        Scanner sc = new Scanner(System.in);
        System.out.println("========== ROOM ADVENTURE ==========");
        System.out.println("Commands: look, go <direction>, take <item>, "
                + "drop <item>, use <item>, check inventory, quit");
        System.out.println("====================================\n");

        while (true) {
            // Show current room and inventory
            System.out.println(currentRoom);
            System.out.println("Inventory: " + inventory);

            System.out.print("\nWhat do you do? ");
            String input = sc.nextLine().trim().toLowerCase();
            if (input.equals("quit") || input.equals("exit")) break;

            String[] words = input.split(" ");
            String verb = words[0];
            String noun = (words.length > 1) ? words[1] : "";

            String response = "I don't understand.";

            //--------------------------------------------------------
            // look
            //--------------------------------------------------------
            if (verb.equals("look")) {
                response = currentRoom.toString();
            }

            //--------------------------------------------------------
            // go
            //--------------------------------------------------------
            else if (verb.equals("go")) {
                response = "You can’t go that way.";
                for (int i = 0; i < currentRoom.getExits().size(); i++) {
                    if (noun.equals(currentRoom.getExits().get(i))) {
                        Room nextRoom = currentRoom.getExitLocations().get(i);
                        if (nextRoom == null) {
                            System.out.println("You stepped into darkness... Game over!");
                            sc.close();
                            return;
                        } else {
                            currentRoom = nextRoom;
                            response = "You move " + noun + ".";
                        }
                        break;
                    }
                }
            }

            //--------------------------------------------------------
            // take
            //--------------------------------------------------------
            else if (verb.equals("take")) {
                response = "You don’t see that here.";
                if (currentRoom.getGrabbables().contains(noun)) {
                    inventory.add(noun);
                    currentRoom.delGrabbable(noun);
                    response = "You took the " + noun + ".";
                }
            }

            //--------------------------------------------------------
            // drop  (Feature #1)
            //--------------------------------------------------------
            else if (verb.equals("drop")) {
                if (inventory.contains(noun)) {
                    inventory.remove(noun);
                    currentRoom.addGrabbable(noun);
                    response = "You dropped the " + noun + ".";
                } else {
                    response = "You don’t have that item.";
                }
            }

            //--------------------------------------------------------
            // use  (Feature #2)
            //--------------------------------------------------------
            else if (verb.equals("use")) {
                if (!inventory.contains(noun)) {
                    response = "You don’t have that item.";
                } else {
                    if (noun.equals("key")) {
                        currentRoom.addExit("south", new Room("Secret Room"));
                        inventory.remove("key");
                        response = "You used the key to unlock a secret door!";
                    } else if (noun.equals("torch")) {
                        response = "You light the torch and see hidden markings on the wall.";
                    } else {
                        response = "You can’t use that right now.";
                    }
                }
            }

            //--------------------------------------------------------
            // check inventory
            //--------------------------------------------------------
            else if (verb.equals("check") && noun.equals("inventory")) {
                if (inventory.isEmpty()) response = "Your inventory is empty.";
                else response = "You’re carrying: " + inventory;
            }

            System.out.println(response);
            System.out.println("------------------------------------");
        }

        sc.close();
        System.out.println("Thanks for playing!");
    }
}
