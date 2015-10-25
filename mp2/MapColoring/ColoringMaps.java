/*
 * @Author Jakub Klapacz <jklapac2@illinois.edu>
 * @Author Abhishek Nigam <adnigam2@illinois.edu>
 *
 */

import java.util.*;

//Optimize this to actually take in a standard matrix representation of a graph!!!
public class ColoringMaps{

	//this will be an array that actually represents the graph
	int map[][];

	//setting these as static and as final so that no class changes these values
	static final int NONE = 0;
	static final int RED = 1;
	static final int YELLOW = 2;
	static final int GREEN = 3;
	static final int BLUE = 4;

	//this should be the number of nodes in the graph, all initialized to no color(NONE) upfront
	int mapColors[];


	void make(){
		//this is your graph


		//each node has a list of nodes that it is connected to.

		
		int x = 12;
		map = new int[x][];
		//map1
		// map[0] = new int[] { 1, 4, 2, 5 };
	 //    map[1] = new int[] { 0, 4, 6, 5 }; 
	 //    map[2] = new int[] { 0, 4, 3, 6, 5 }; 
	 //    map[3] = new int[] { 2, 4, 6 }; 
	 //    map[4] = new int[] { 0, 1, 6, 3, 2 }; 
	 //    map[5] = new int[] { 2, 6, 1, 0 }; 
	 //    map[6] = new int[] { 2, 3, 4, 1, 5 };

		//map 2 -- Australia
		// int WA  = 0;
		// int NT  = 1;
		// int SA  = 2;
		// int Q   = 3;
		// int NSW = 4;
		// int V   = 5;
		// int T   = 6;

		// map[T] 		= new int[] {};
	 //    map[WA] 	= new int[] {NT, SA};
	 //   	map[NT] 	= new int[] {WA, Q, SA};
	 //   	map[SA] 	= new int[] {WA, NT, Q, NSW, V};
	 //    map[Q] 		= new int[]  {NT, SA, NSW   };
	 //    map[NSW] 	= new int[] {Q, SA, V};
  //       map[V]  	= new int[] {SA, NSW};

		map[0] = new int[] {1, 4, 5};
		map[1] = new int[] {0, 3};
		map[2] = new int[] {};
		map[3] = new int[] {1};
		map[4] = new int[] {0};
		map[5] = new int[] {0,6,11};
		map[6] = new int[] {5};
		map[7] = new int[] {8,9,11};
		map[8] = new int[] {7}; 
		map[9] = new int[] {7,10};
		map[10] = new int[] {9};
		map[11] = new int[] {5,7};

	    mapColors = new int[x];
		for(int i = 0; i<x;i++)
			mapColors[i] = NONE;
	}	

	boolean search(int node, int color){
		if(node >= map.length) return true;
		//if(canContinue(node, color)){
			mapColors[node] = color;
			for(int i = RED; i <= BLUE; i++){
				if(search(node+1, i)) return true;
			}
		//}
		return false;
	}

	boolean canContinue(int node, int color){
		//check if any adjacent nodes have the same color
		for(int i = 0; i< map[node].length; i++){
			int adjacent = map[node][i];
			if(mapColors[adjacent] == color) return false;
		}
		//if none of them do, return true.
		return true;
	}

	void print(){
		for(int i = 0; i<mapColors.length;i++){
			System.out.print("Node " + i + " is " );
			switch(mapColors[i]){
				case NONE: 
					System.out.println("none?!"); break;
				case RED:
					System.out.println("red"); break;
				case YELLOW:
					System.out.println("yellow"); break;
				case GREEN:
					System.out.println("green"); break;
				case BLUE:
					System.out.println("blue"); break;
			}
		}
	}

	public static void main(String [] args){
		ColoringMaps mappy = new ColoringMaps();
		mappy.make();
		boolean final_val = mappy.search(0, RED);
		if(final_val)
			mappy.print();
		else
			System.out.println("No solution found");
	}
}