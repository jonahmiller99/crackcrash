import numpy as np
import pandas as pd

# Convert the data collections into lists

data_pd = pd.read_csv('12_hour_crash_data.csv')
data = [i[1] for i in data_pd.to_numpy()]

new_data_pd = pd.read_csv('15_hour_crash_data.csv')
newdata = [tuple(j[1:]) for j in new_data_pd.to_numpy()]

# This is the data set used for actual analysis since it is the largest
full_day_data_pd = pd.read_csv('24_hour_crash_data.csv')
fulldaydata = [tuple(k[1:]) for k in full_day_data_pd.to_numpy()]

print(len(data))
# 1645 data points in ~12 hours of collection
print(len(newdata))
# 2405 data points in ~15 hours of collection
print(len(fulldaydata))
# 3122 data points in ~24 hours of collection

# first for loop runs through all the multiplier values in the data array
# second for loop runs through every integer 0-3000 to see if it would be a win or loss at that value
# for first number in "data" multiplier = 2.01 .... inside the inner loop 1 and 2 would be winners
# (2,3000] would be down $1
# index of win loss is how much you would be up or down after this session if for every
# turn you pulled money at that multiplier

total_one = 0
count1 = 0
count2 = 0
max_bet_array = np.arange(7000)
win_loss_array = np.zeros(7000)

for i in range(len(fulldaydata)):
    for x in range(7000):

        if fulldaydata[i][0] <= max_bet_array[x]:
            win_loss_array[x] -= 1
            count1 += 1
        else:
            win_loss_array[x] += (max_bet_array[x] - 1)
            count2 += 1

print(max(win_loss_array))  # this is = $3877.00
print(win_loss_array[50])   # this is = $-622.00
print(win_loss_array[100])  # this is = $-22.00
print(win_loss_array[200])  # this is = $678.00
print(win_loss_array[300])  # this is = $778.00
print(win_loss_array[500])  # this is = $1378.00

val = np.where(win_loss_array == 3877)  # Max Profit is at 7000x multiplier

# if you used martingale strategy in this time span
# and there was a sequence of 10 sub 2 runs in a row
# thus you would need 2048x what your first bet was to maintain this strategy, actual loss was worse than this

gamblers_fallacy_max_loss = 0
counter = 0

for i in range(len(fulldaydata) - 1):
    counter = 0
    while fulldaydata[i][0] < 2:
        counter += 1
        if counter > gamblers_fallacy_max_loss:
            gamblers_fallacy_max_loss = counter
        i += 1

# max amount of games lost in around = gamblers_fallacy_max_loss
# martingale requires you to double your bet each loss in order to make money back
# will need (2^(gamblers_fallacy_max_loss + 1))*(initial bet amount) to play this strategy
gamblers_fallacy_max_loss += 1

bankrollrequired = 2 ** gamblers_fallacy_max_loss

print(("Martingale Strategy Bankroll Needed = {} times initial bet").format(bankrollrequired))

# Using the data collected the
# Martingale Strategy Bankroll Needed = 8192 times initial bet





#################  Main Analysis #####################

EV = 0
EV_arr = []
EV_arr.clear()
c1 = 0
c2 = 0

withdrawlNum = 200

for i in range(len(fulldaydata)):
    if (fulldaydata[i][0] < withdrawlNum):
        EV = EV - 1
        EV_arr.append(EV)
        c1 += 1
    else:
        EV += withdrawlNum - 1
        EV_arr.append(EV)
        c2 += 1

print("Multiplier played this session: {}".format(withdrawlNum))
if EV < 0:
    print("End session down: {}".format(EV))
else:
    print("End session up: {}".format(EV))

print("Number of Winning Games: {}".format(c2))
print("Maximum amount down: {}".format(min(EV_arr)))


###  ~~~~~~~~~~~  Results ~~~~~~~~~~~~~ ###
# This shows that if you were to use the 200x multiplier as stop point
# You would end the session up $678.00
# Most you would ever go down was -$347.00
# Number of Winning Games: 19