/* Dynamic predicates - predicates that might change during execution */
/* Number after slash dennotes number of arguments */
:- dynamic([
    reborn/0,
    visited/2,
    current/3,
    move/2,
    hasarrow/0,
    wumpus/2,
    stench/2,
    confundus/2,
    safe/2,
    moveforward/0,
    turnleft/0,
    turnright/0,
    pickup/0,
    shoot/0,
    tingle/2,
    wall/2,
    reposition/1,
    glitter/2,
    safeandunvisited/2,
    explore/1,
    exploremap/1,
    returntoorigin/1,
    dfs/3,
    dfshome/3,
    currentcopy/3,
    movements/1,
    apply_safe/2,
    apply_confundus/2,
    apply_wumpus/2,
    origin/2,
    wumpusalive/0
]).

/*  ---------- Reposition ---------- */
reposition(L) :-
    current(X,Y,_),
    (
        /* Confounded, Stench, Tingle, Glitter, Bump, Scream. */
        (
            L = [on,on,on,_,_,_] -> (
                (wumpusalive -> assert(stench(X,Y));true),
                assert(tingle(X,Y)),
                
                assert(visited(X,Y)),
                assert(safe(X,Y)),
                assert(origin(X,Y)),

                apply_confundus(X,Y),
                apply_wumpus(X,Y)
            )
        );
        (
            L = [on,on,_,_,_,_] -> (
                (wumpusalive -> assert(stench(X,Y));true),

                assert(visited(X,Y)),
                assert(safe(X,Y)),
                assert(origin(X,Y)),

                apply_wumpus(X,Y)
            )
        );
        (
            L = [on,_,on,_,_,_] -> (
                assert(tingle(X,Y)),
                
                assert(visited(X,Y)),
                assert(safe(X,Y)),
                assert(origin(X,Y)),

                apply_confundus(X,Y)
            )
        );
        (
            L = [on,_,_,_,_,_] -> (
                assert(visited(X,Y)),
                assert(safe(X,Y)),
                assert(origin(X,Y)),

                apply_safe(X,Y)
            )
        )
    ).

/* Move */
move(A,L) :- 
    current(X,Y,Orientation),
    (
        /* Confounded, Stench, Tingle, Glitter, Bump, Scream. */
        (
            /* Wumpus killed */
            A = shoot, L = [_,_,_,_,_,on] -> (
                retractall(stench(_,_)),
                retractall(wumpus(_,_)),
                retract(wumpusalive)
            )
        );
        (
            /* Hits a wall */
            A = moveforward, L = [_,_,_,_,on,_] -> (
                assert(wall(X,Y)),
                /* Move back */
                (
                    Orientation = rnorth, NewX is X, NewY is Y - 1;
                    Orientation = rsouth, NewX is X, NewY is Y + 1;
                    Orientation = rwest, NewX is X + 1, NewY is Y;
                    Orientation = reast, NewX is X - 1, NewY is Y
                ),
                retract(current(_,_,_)),
                assert(current(NewX, NewY, Orientation)),
                /* If safe, confundus or wumpus cell previously, retract it */
                (safe(X,Y) -> retract(safe(X,Y));true),
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Confounded */
            A = moveforward, L = [on,_,_,_,_,_] -> (
                retractall(current(_,_,_)),
                assert(current(0, 0, rnorth)),
                retractall(stench(_,_)),
                retractall(wumpus(_,_)),
                retractall(tingle(_,_)),
                retractall(confundus(_,_)),
                retractall(visited(_,_)),
                retractall(safe(_,_)),
                retractall(wall(_,_)),
                retractall(glitter(_,_)),
                retractall(origin(_,_))
            )
        );
        (
            /* Stench, tingle, and glitter */
            A = moveforward, L = [_,on,on,on,_,_] -> (
                (wumpusalive -> assert(stench(X,Y));true),
                assert(tingle(X,Y)), 
                assert(glitter(X,Y)), 

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_confundus(X,Y),
                apply_wumpus(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Stench and glitter */
            A = moveforward, L = [_,on,_,on,_,_] -> (
                (wumpusalive -> assert(stench(X,Y));true),
                assert(glitter(X,Y)), 

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_wumpus(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Tingle and glitter */
            A = moveforward, L = [_,_,on,on,_,_] -> (
                assert(tingle(X,Y)),
                assert(glitter(X,Y)), 

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_confundus(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Glitter */
            A = moveforward, L = [_,_,_,on,_,_] -> (
                assert(glitter(X,Y)),

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_safe(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Stench and Tingle */
            A = moveforward, L = [_,on,on,_,_,_] -> (
                (wumpusalive -> assert(stench(X,Y));true),
                assert(tingle(X,Y)), 

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_confundus(X,Y),
                apply_wumpus(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Stench */
            A = moveforward, L = [_,on,_,_,_,_] -> (
                (wumpusalive -> assert(stench(X,Y));true),

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_wumpus(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Tingle */
            A = moveforward, L = [_,_,on,_,_,_] -> (
                assert(tingle(X,Y)),

                assert(visited(X,Y)),
                assert(safe(X,Y)),

                apply_confundus(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        );
        (
            /* Nothing */
            A = moveforward, L = [off,off,off,off,off,off] -> (
                assert(visited(X,Y)),
                assert(safe(X,Y)),
                
                apply_safe(X,Y),

                /* If confundus or wumpus cell previously, retract it since cell is technically safe */
                (confundus(X,Y) -> retract(confundus(X,Y));true),
                (wumpus(X,Y) -> retract(wumpus(X,Y));true)
            )
        )   
    ).

/*  ---------- Stench and Wumpus ---------- */
stench :- false.
wumpus :- false.

wumpusalive.

apply_wumpus(X,Y) :-
    wumpusalive,
    N is Y + 1, 
    S is Y - 1,
    W is X - 1,
    E is X + 1,
    (
        not(safe(X,N)),not(wall(X,N)),not(wumpus(X,N)) -> assert(wumpus(X,N));true  
    ),
    (
        not(safe(X,S)),not(wall(X,S)),not(wumpus(X,S)) -> assert(wumpus(X,S));true
    ),
    (
        not(safe(W,Y)),not(wall(W,Y)),not(wumpus(W,Y)) -> assert(wumpus(W,Y));true
    ),
    (
        not(safe(E,Y)),not(wall(E,Y)),not(wumpus(E,Y)) -> assert(wumpus(E,Y));true
    ).

/*  ---------- Tingle and Confundus ---------- */
tingle :- false.
confundus :- false.

apply_confundus(X,Y) :-
    N is Y + 1, 
    S is Y - 1,
    W is X - 1,
    E is X + 1,
    (
        not(safe(X,N)),not(wall(X,N)),not(confundus(X,N)) -> assert(confundus(X,N));true  
    ),
    (
        not(safe(X,S)),not(wall(X,S)),not(confundus(X,S)) -> assert(confundus(X,S));true
    ),
    (
        not(safe(W,Y)),not(wall(W,Y)),not(confundus(W,Y)) -> assert(confundus(W,Y));true
    ),
    (
        not(safe(E,Y)),not(wall(E,Y)),not(confundus(E,Y)) -> assert(confundus(E,Y));true
    ).

/*  ---------- Wall ---------- */
wall:- false.

/*  ---------- Initial positions ---------- */
current(0,0,rnorth).

/*  ---------- Reborn ---------- */
reborn :-
    retractall(current(_,_,_)),
    assert(current(0, 0, rnorth)),
    retractall(stench(_,_)),
    retractall(wumpus(_,_)),
    retractall(tingle(_,_)),
    retractall(confundus(_,_)),
    retractall(visited(_,_)),
    retractall(safe(_,_)),
    retractall(wall(_,_)),
    retractall(glitter(_,_)),
    retractall(origin(_,_)),
    assert(hasarrow),
    assert(wumpusalive).

/*  ---------- Visited ---------- */
visited :- false.

/*  ---------- Safe ---------- */
apply_safe(X,Y) :-
    N is Y + 1, 
    S is Y - 1,
    W is X - 1,
    E is X + 1,
    (
        not(safe(X,N)),not(wall(X,N)) -> assert(safe(X,N));true  
    ),
    (
        not(safe(X,S)),not(wall(X,S)) -> assert(safe(X,S));true
    ),
    (
        not(safe(W,Y)),not(wall(W,Y)) -> assert(safe(W,Y));true  
    ),
    (
        not(safe(E,Y)),not(wall(E,Y)) -> assert(safe(E,Y));true  
    ).


/*  ---------- Actions ---------- */
moveforward :-
    current(X,Y,Orientation),
    (
        Orientation = rnorth, NewX is X, NewY is Y + 1;
        Orientation = rsouth, NewX is X, NewY is Y - 1;
        Orientation = rwest, NewX is X - 1, NewY is Y;
        Orientation = reast, NewX is X + 1, NewY is Y
    ),
    retract(current(_,_,_)),
    assert(current(NewX, NewY, Orientation)). 

turnleft :- 
    current(X,Y,Orientation),
    (
        Orientation = rnorth, NewOrientation = rwest;
        Orientation = rsouth, NewOrientation = reast;
        Orientation = rwest, NewOrientation = rsouth;
        Orientation = reast, NewOrientation = rnorth
    ),
    retract(current(_,_,_)),
    assert(current(X,Y,NewOrientation)).

turnright :- 
    current(X,Y,Orientation),
    (
        Orientation = rnorth, NewOrientation = reast;
        Orientation = rsouth, NewOrientation = rwest;
        Orientation = rwest, NewOrientation = rnorth;
        Orientation = reast, NewOrientation = rsouth
    ),
    retract(current(_,_,_)),
    assert(current(X,Y,NewOrientation)).

pickup :-
    current(X,Y,_),
    retract(glitter(X,Y)).

shoot:- 
    (
        hasarrow -> (
            write('Agent shoots.\n')
        );
        write('Agent does not have an arrow.\n')
    ),
    retract(hasarrow).
    

/*  ---------- Arrow ---------- */
hasarrow.

/*  ---------- Explore Main ---------- */
safeandunvisited(X,Y) :- 
    safe(X,Y),
    not(visited(X,Y)).

explore(L) :- 
    current(AgentX,AgentY,_),
    findall([X,Y],safeandunvisited(X,Y),SAV),
    (
        SAV = [] -> 
            (
                write('There are no more safe and visited cells.\n'),
                (
                    AgentX is 0, AgentY is 0 -> write('Agent is now back to the relative origin cell.\n'), retractall(explore(L));
                    write('Agent will now return to the relative origin cell.\n')
                ),
                returntoorigin(L)
            );
            (
                write('Agent will move to the next safe and unvisited cell.\n'),
                exploremap(L)
            )
    ).

/* BFS to find a path to a safe and unvisited cell */
exploremap(L) :-
    current(X,Y,_),
    first_solution(Solution,[dfs([],[X,Y],Solution)],[]),
    reverse(Solution, Result),
    retractall(movements(_)),
    loop(Result),
    (findall(Action, movements(Action), L),!).

/* BFS to find a path back to origin */
returntoorigin(L) :-
    current(X,Y,_),
    first_solution(Solution,[dfshome([],[X,Y],Solution)],[]),
    reverse(Solution, Result),
    retractall(movements(_)),
    loop(Result),
    (findall(Action, movements(Action), L),!).
    
dfs(Path,[X,Y],[[X,Y]|Path]):-
    safeandunvisited(X,Y).

dfs(Path,[X,Y],Sol):-
    safeandunvisited(NewX,NewY),
    (   
    	(NewX is X,NewY is Y+1);
	    (NewX is X,NewY is Y-1);
	    (NewY is Y,NewX is X+1);
    	(NewY is Y,NewX is X-1)
    ),
    not(member([NewX,NewY],Path)),
    dfs([[X,Y]|Path],[NewX,NewY],Sol).

dfs(Path,[X,Y],Sol):-
    safe(NewX,NewY),
    (   
    	(NewX is X,NewY is Y+1);
	    (NewX is X,NewY is Y-1);
	    (NewY is Y,NewX is X+1);
    	(NewY is Y,NewX is X-1)
    ),
    not(member([NewX,NewY],Path)),
    dfs([[X,Y]|Path],[NewX,NewY],Sol).

dfshome(Path,[X,Y],[[X,Y]|Path]):-
    origin(X,Y).
    
dfshome(Path,[X,Y],Sol):-
    safe(NewX,NewY),
    (   
    	(NewX is X,NewY is Y+1);
	    (NewX is X,NewY is Y-1);
	    (NewY is Y,NewX is X+1);
    	(NewY is Y,NewX is X-1)
    ),
    not(member([NewX,NewY],Path)),
    dfshome([[X,Y]|Path],[NewX,NewY],Sol).

loop([]). 
loop([H|T]) :- process(H), loop(T).

movements().

process(H) :-
    current(X,Y,Z),
    (
        /* If first loop, simply assert it as currentcopy */
    	H \= [X,Y] -> (
            not(wall(X,Y)),
            nth0(0, H, CurX),
        	nth0(1, H, CurY),
            currentcopy(PrevX,PrevY,PrevZ),
            N is PrevY + 1,
            S is PrevY - 1,
            W is PrevX - 1,
            E is PrevX + 1,
			(	
            	CurX = PrevX, CurY = N, PrevZ = rnorth -> assertz(movements(moveforward)), NewD = rnorth;
	            CurX = PrevX, CurY = S, PrevZ = rnorth -> assertz(movements(turnleft)), assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = rsouth;
	            CurX = W, CurY = PrevY, PrevZ = rnorth -> assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = rwest;
            	CurX = E, CurY = PrevY, PrevZ = rnorth -> assertz(movements(turnright)), assertz(movements(moveforward)), NewD = reast;
            
            	CurX = PrevX, CurY = N, PrevZ = rsouth -> assertz(movements(turnleft)), assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = rnorth;	
	            CurX = PrevX, CurY = S, PrevZ = rsouth -> assertz(movements(moveforward)), NewD = rsouth;
	            CurX = W, CurY = PrevY, PrevZ = rsouth -> assertz(movements(turnright)), assertz(movements(moveforward)), NewD = rwest;
            	CurX = E, CurY = PrevY, PrevZ = rsouth -> assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = reast;
            
            	CurX = PrevX, CurY = N, PrevZ = rwest -> assertz(movements(turnright)), assertz(movements(moveforward)), NewD = rnorth;	
	            CurX = PrevX, CurY = S, PrevZ = rwest -> assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = rsouth;
	            CurX = W, CurY = PrevY, PrevZ = rwest -> assertz(movements(moveforward)), NewD = rwest;
            	CurX = E, CurY = PrevY, PrevZ = rwest -> assertz(movements(turnleft)), assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = reast;
            
            	CurX = PrevX, CurY = N, PrevZ = reast -> assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = rnorth;	
	            CurX = PrevX, CurY = S, PrevZ = reast -> assertz(movements(turnright)), assertz(movements(moveforward)), NewD = rsouth;
	            CurX = W, CurY = PrevY, PrevZ = reast -> assertz(movements(turnleft)), assertz(movements(turnleft)), assertz(movements(moveforward)), NewD = rwest;
            	CurX = E, CurY = PrevY, PrevZ = reast -> assertz(movements(moveforward)), NewD = reast
            ),
            retract(currentcopy(_,_,_)),
            assert(currentcopy(CurX,CurY,NewD))
     	);
        (
            /* Check if coin */
            findall([X,Y], glitter(X,Y), COIN),
            (
                member([X,Y],COIN) -> assertz(movements(pickup));true
            ),
            retractall(currentcopy(_,_,_)),
            assert(currentcopy(X,Y,Z))
        )
    ).

/* ------------------------------------------------------------------------------ */