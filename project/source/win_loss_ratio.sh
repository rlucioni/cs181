#/bin/sh

games=$1

wins=0
losses=0
ties=0

for x in $(seq 1 $games)
do
    output=`python run_game.py -d 0 | tail -n 1`
    case $output in
        "Player 1"*)
            wins=$[wins+1]
            ;;
        "Player 2"*)
            losses=$[losses+1]
            ;;
        "Tie"*)
            ties=$[ties+1]
            ;;
        *)
            #echo "Could not match."
            echo $output
            ;;
    esac
done

echo $wins":"$losses":"$ties
