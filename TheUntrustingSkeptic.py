from prison import Player

class UntrustingSkepticPlayer(Player):

    collusionCode = [0, 0, 0, 1, 0, 1, 0, 0]
    isColluding = False

    @staticmethod
    def reset():
        UntrustingSkepticPlayer.isColluding = False

    #Checks if an opponent played the collusion code
    def isFriend(self, playerHistory):
        if len(playerHistory) < 8: 
            return False

        mismatchCount = 0
        for i in range(8):
            if UntrustingSkepticPlayer.collusionCode[i] != playerHistory[i]:
                mismatchCount += 1

        if mismatchCount <= 1:
            return True

        return False

    #Checks if colluder is continuing to collude 
    def isStillFriend(self, playerHistory):
        defectCount = 0
        for i in range(1, 11):
            if playerHistory[-i] == 1:
                defectCount += 1

        if defectCount <= 1:
            return True

        return False


    #Checks if this player has cooperated for the last 9 plays
    def obeyedCollusionSoFar(self, myHistory):
        defectCount = 0
        for i in range(1, 10):
            if myHistory[-i] == 1:
                defectCount += 1

        if defectCount == 0:
            return True
        else:
            return False
        
    def studentID(self):
        return "20706783"

    def agentName(self):
        return "The Untrusting Skeptic"


    # Collude 
    def playCollusion(self, myHistory, oppHistory1, oppHistory2, turn):
        if turn <= 8:
            return UntrustingSkepticPlayer.collusionCode[turn - 1]
        elif turn % 10 == 8 and self.obeyedCollusionSoFar(myHistory):
            return 1
        else:
            return 0
    
    # The player's own strategy
    def playMyStrategy(self, myHistory, oppHistory1, oppHistory2, turn):
        defectCountOpp1 = 0
        defectCountOpp2 = 0

        if turn == 1:
            return 0
        elif turn > 10:
            for i in range(1, 11):
                if oppHistory1[-i] == 1:
                    defectCountOpp1 += 1
                if oppHistory2[-i] == 1:
                    defectCountOpp2 += 1

            # Cooperate only if both oppoents cooperated most of the times in the last 10 plays
            if defectCountOpp1 <= 2 and defectCountOpp2 <= 2:
                return 0
            else: 
                return 1
        
        # Modified TFT for a short duration...upto 10th play
        if oppHistory1[-1] == 1 and oppHistory2[-1] == 1:
            return 1
        elif oppHistory1[-1] + oppHistory1[-2] == 1 and oppHistory2[-1] + oppHistory2[-2] == 1:
            return 1
        else:
            return 0


    def play(self, myHistory, oppHistory1, oppHistory2):

        currentTurn = len(myHistory) + 1

        #Reset state at start of the game
        if currentTurn == 1:
            UntrustingSkepticPlayer.reset()

         # Play the collusion code for first 8 plays   
        if currentTurn <= 8:
            return self.playCollusion(myHistory, oppHistory1, oppHistory2, currentTurn)

        # Check for colluders in the 9th play
        elif currentTurn == 9:
            if self.isFriend(oppHistory1) and self.isFriend(oppHistory2):
                UntrustingSkepticPlayer.isColluding = True

            if UntrustingSkepticPlayer.isColluding:
                return self.playCollusion(myHistory, oppHistory1, oppHistory2, currentTurn)

        # Check point for making sure colluders are continuing to collude
        elif currentTurn % 10 == 9 and UntrustingSkepticPlayer.isColluding:
            if not self.isStillFriend(oppHistory1) or  not self.isStillFriend(oppHistory2):
                UntrustingSkepticPlayer.isColluding = False

            if UntrustingSkepticPlayer.isColluding:
                return self.playCollusion(myHistory, oppHistory1, oppHistory2, currentTurn)

         # Play nice as long as there is collusion       
        elif UntrustingSkepticPlayer.isColluding:
            return self.playCollusion(myHistory, oppHistory1, oppHistory2, currentTurn)            
           
        # If no collusion or collusion is broken, then play my own strategy   
        return self.playMyStrategy(myHistory, oppHistory1, oppHistory2, currentTurn)
