from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
import pandas as pd
import math as m
import matplotlib.pylab as plt
plt.style.use('seaborn-darkgrid')

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)


def getNumber(last, first):
    playerTable = playerid_lookup(last, first)
    playerTable = playerTable.loc[playerTable['mlb_played_last'].isin([2019])]
    playerTable.index = range(len(playerTable['mlb_played_last']))
    number = playerTable['key_mlbam']
    number = number[0]
    return number


def dataGrab(number, start, end):
    data = statcast_pitcher(start_dt=start, end_dt=end,
                            player_id=number)
    data = data[['pitch_type', 'release_speed', 'effective_speed',
                 'release_pos_x', 'plate_x', 'release_pos_z', 'plate_z',
                 'release_extension', 'zone', 'launch_speed', 'launch_angle',
                 'estimated_woba_using_speedangle']]
    data.index = range(len(data['pitch_type']))
    return data


def release_data_per(before, after, end, begin):
    pitch_types = ['CH', 'CU', 'FC', 'FF', 'FO', 'FS', 'FT', 'GY', 'KC', 'KN',
                   'SC', 'SI', 'SL', 'EP']
    before = before.loc[before['pitch_type'].isin(pitch_types)]
    after = after.loc[after['pitch_type'].isin(pitch_types)]
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    pitches = []
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        date = 'Before ' + end
        name = countsB.index[i]
        avgVelo = round(pitchData['release_speed'].dropna().mean(), 1)
        avgEffSpeed = round(pitchData['effective_speed'].mean(), 1)
        averageRelExt = round(pitchData['release_extension'].mean(), 2)
        averageRelX = round(pitchData['plate_x'].mean(), 2)
        averageRelZ = round(pitchData['plate_z'].mean(), 2)
        pitch = [date, name, avgVelo, avgEffSpeed, averageRelExt,
                 averageRelX, averageRelZ]
        pitches.append(pitch)
    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        date = 'After ' + begin
        name = countsA.index[i]
        avgVelo = round(pitchData['release_speed'].dropna().mean(), 1)
        avgEffSpeed = round(pitchData['effective_speed'].mean(), 1)
        averageRelExt = round(pitchData['release_extension'].mean(), 2)
        averageRelX = round(pitchData['plate_x'].mean(), 2)
        averageRelZ = round(pitchData['plate_z'].mean(), 2)
        pitch = [date, name, avgVelo, avgEffSpeed, averageRelExt,
                 averageRelX, averageRelZ]
        pitches.append(pitch)
    pitches = pd.DataFrame(pitches, columns=['Before/After', 'Name',
                                             'Average_Velocity',
                                             'Effective_Speed',
                                             'Release_Extension',
                                             'Horizontal_Break',
                                             'Vertical_Break'])
    pitches = pitches.sort_values(by=['Name', 'Before/After'], ascending=False)
    return pitches


def plot_release_data_per(before, after, end, begin):
    pitch_types = ['CH', 'CU', 'FC', 'FF', 'FO', 'FS', 'FT', 'GY', 'KC', 'KN',
                   'SC', 'SI', 'SL', 'EP']
    before = before.loc[before['pitch_type'].isin(pitch_types)]
    after = after.loc[after['pitch_type'].isin(pitch_types)]
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    fig, axes = plt.subplots(nrows=3, ncols=1)
    fig.set_size_inches(8, 8, forward=True)
    fig.subplots_adjust(hspace=0.25, top=.95, bottom=.05, right=.95, left=.1)
    ax0, ax1, ax2 = axes.flatten()
    ax0.plot([.79, .79, -.79, -.79, .79], [3.5, 1.5, 1.5, 3.5, 3.5],
             color='red', label='K Zone')
    ax0.plot([.94, .94, -.94, -.94, .94], [3.73, 1.27, 1.27, 3.73, 3.73],
             color='red', label='Outer Limits of K Zone', ls=':', alpha=0.5)
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        name = countsB.index[i]
        avgVelo = round(pitchData['release_speed'].dropna().mean(), 1)
        avgEffSpeed = round(pitchData['effective_speed'].dropna().mean(), 1)
        averageRelX = round(pitchData['plate_x'].dropna().mean(), 2)
        averageRelZ = round(pitchData['plate_z'].dropna().mean(), 2)
        label = name + ' Before'
        ax0.scatter(averageRelX, averageRelZ, label=label, s=100)
        ax1.bar(label, avgVelo)
        ax1.text(label, 70, s=round(avgVelo, 1), color='white',
                 horizontalalignment='center', verticalalignment='center')
        ax2.bar(label, avgEffSpeed)
        ax2.text(label, 70, s=round(avgEffSpeed, 1), color='white',
                 horizontalalignment='center', verticalalignment='center')
    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        name = countsA.index[i]
        avgVelo = round(pitchData['release_speed'].dropna().mean(), 1)
        avgEffSpeed = round(pitchData['effective_speed'].dropna().mean(), 2)
        averageRelX = round(pitchData['plate_x'].dropna().mean(), 2)
        averageRelZ = round(pitchData['plate_z'].dropna().mean(), 2)
        label = name + ' After'
        ax0.scatter(averageRelX, averageRelZ, label=label, s=100)
        ax1.bar(label, avgVelo)
        ax1.text(label, 70, s=round(avgVelo, 1), color='white',
                 horizontalalignment='center', verticalalignment='center')
        ax2.bar(label, avgEffSpeed)
        ax2.text(label, 70, s=round(avgEffSpeed, 1), color='white',
                 horizontalalignment='center', verticalalignment='center')

    ax0.legend(prop={'size': 7})
    ax0.set_title('Average Location at the Plate (Catcher\'s View)')
    ax0.set_xlim(-3, 3)
    ax0.set_ylim(1, 4)
    ax0.get_xaxis().set_visible(False)
    ax0.get_yaxis().set_visible(False)
    ax1.set_title('Average Velocity per Pitch')
    ax1.set_ylim(67, 102)
    ax1.set_ylabel('Velocity (mph)')
    ax2.set_title('Average Effective Velocity per Pitch')
    ax2.set_ylim(67, 102)
    ax2.set_ylabel('Effective Velocity (mph)')


# have to have this as most data points are null for launch speed/angle
def bat_exit_per(before, after, end, begin):
    before = before[['pitch_type', 'launch_speed', 'launch_angle',
                     'estimated_woba_using_speedangle']].dropna()
    after = after[['pitch_type', 'launch_speed', 'launch_angle',
                   'estimated_woba_using_speedangle']].dropna()
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    pitches = []
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        pitchData = pitchData.dropna()
        dateB = 'Before ' + end
        name = countsB.index[i]
        lauchSpeedB = round(pitchData['launch_speed'].mean(), 2)
        launchAngleB = round(pitchData['launch_angle'].mean(), 2)
        avgwOBA = round(pitchData['estimated_woba_using_speedangle'].mean(), 3)
        pitch = [dateB, name, lauchSpeedB, launchAngleB, avgwOBA]
        pitches.append(pitch)

    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        dateB = 'After ' + begin
        name = countsA.index[i]
        launchSpeedA = round(pitchData['launch_speed'].mean(), 2)
        launchAngleA = round(pitchData['launch_angle'].mean(), 2)
        avgwOBA = round(pitchData['estimated_woba_using_speedangle'].mean(), 2)
        pitch = [dateB, name, launchSpeedA, launchAngleA, avgwOBA]
        pitches.append(pitch)
    pitches = pd.DataFrame(pitches, columns=['Before/After', 'Name',
                                             'Launch_Speed', 'Launch_Angle',
                                             'Average_wOBA'])
    return pitches


def plot_bat_exit_per(before, after, end, begin):
    before = before[['pitch_type', 'launch_speed', 'launch_angle',
                     'estimated_woba_using_speedangle']].dropna()
    after = after[['pitch_type', 'launch_speed', 'launch_angle',
                   'estimated_woba_using_speedangle']].dropna()
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    fig, axes = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches(6, 6)
    fig.subplots_adjust(top=.9, bottom=.05, right=.95, left=.05)
    ax = plt.subplot(111, projection='polar')
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        pitchData = pitchData.dropna()
        name = countsB.index[i]
        launchSpeed = round(pitchData['launch_speed'].mean(), 2)
        launchAngle = round(pitchData['launch_angle'].mean(), 2)
        avgwOBA = round(pitchData['estimated_woba_using_speedangle'].mean(), 2)
        label = name + ' Before'
        ax.scatter(m.radians(launchAngle), launchSpeed, s=avgwOBA*200,
                   label=label)
    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        name = countsA.index[i]
        launchSpeed = round(pitchData['launch_speed'].mean(), 2)
        launchAngle = round(pitchData['launch_angle'].mean(), 2)
        avgwOBA = round(pitchData['estimated_woba_using_speedangle'].mean(), 2)
        label = name + ' After'
        ax.scatter(m.radians(launchAngle), launchSpeed, s=avgwOBA*200,
                   label=label)
    ax.legend(prop={'size': 7})
    ax.set_ylim(0, 120)
    ax.set_xlim(m.pi/2, 0)
    ax.set_xticks([0, m.pi/4, m.pi/2])
    ax.set_yticks([0, 60, 120])
    ax.set_title('Average Launch Angle and Exit Velocity')
    ax.set_xlabel('Launch Angle (Deg.)')
    ax.set_ylabel('Exit Velocity (mph)')


# plotting pitch location
def plot_pitch_location(before, after, first, last, end, begin):
    pitch_types = ['CH', 'CU', 'FC', 'FF', 'FO', 'FS', 'FT', 'GY', 'KC', 'KN',
                   'SC', 'SI', 'SL', 'EP']
    before = before[['pitch_type', 'zone']].dropna()
    after = after[['pitch_type', 'zone']].dropna()
    before = before.loc[before['pitch_type'].isin(pitch_types)]
    after = after.loc[after['pitch_type'].isin(pitch_types)]
    countsB = before['pitch_type'].value_counts(dropna=True)
    countsA = after['pitch_type'].value_counts(dropna=True)
    pitchesBefore = []
    pitchesAfter = []
    fig, axes = plt.subplots(nrows=2, ncols=1)
    fig.set_size_inches(8, 6, forward=True)
    ax0, ax1 = axes.flatten()
    for i in range(len(countsB)):
        is_pitch = before['pitch_type'] == countsB.index[i]
        pitchData = before[is_pitch]
        pitchData = pitchData.dropna()
        name = countsB.index[i]
        popZoneB = pitchData['zone']
        pitch = [name, popZoneB]
        pitchesBefore.append(pitch)
    pitchesBefore = pd.DataFrame(pitchesBefore, columns=['Name', 'Zone'])
    for i in range(len(countsA)):
        is_pitch = after['pitch_type'] == countsA.index[i]
        pitchData = after[is_pitch]
        name = countsA.index[i]
        popZoneA = pitchData['zone']
        pitch = [name, popZoneA]
        pitchesAfter.append(pitch)
    pitchesAfter = pd.DataFrame(pitchesAfter, columns=['Name', 'Zone'])
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    ax0.hist(pitchesBefore['Zone'], bins=bins, density=True,
             stacked=True, label=pitchesBefore['Name'], align='left',
             lw=0.2, edgecolor='black')
    ax0.legend(prop={'size': 10})
    titleB = first + ' ' + last + ' Before ' + end
    ax0.set_title(titleB)
    ax1.hist(pitchesAfter['Zone'], bins=bins, density=True,
             stacked=True, label=pitchesAfter['Name'], align='left',
             lw=0.2, edgecolor='black')
    ax1.legend(prop={'size': 10})
    titleA = first + ' ' + last + ' After ' + begin
    ax1.set_title(titleA)
    fig.tight_layout()
    ax0.set_ylim(0, 0.25)
    ax0.set_xticks(bins[:-1])
    ax0.set_xlabel('Zone')
    ax0.set_ylabel('Density')
    ax1.set_xticks(bins[:-1])
    ax1.set_ylim(0, 0.25)
    ax1.set_xlabel('Zone')
    ax1.set_ylabel('Density')
    fig.subplots_adjust(hspace=0.35, left=0.1, bottom=0.07, right=0.95, top=0.95)


def main():
    pFirst = input('Enter Pitcher\'s First Name: ')
    pLast = input('Enter Pitcher\'s Last Name: ')
    Date1Start = input('Enter First Range Start Date (Example: 2019-3-1 for March 1st, 2019): ')
    Date1End = input('Enter First Rage End Date: ')
    Date2Start = input('Enter Second Range Start Date: ')
    Date2End = input('Enter Second Rage End Date: ')

    # getting all data needed
    number = getNumber(pLast, pFirst)
    before = dataGrab(number, Date1Start, Date1End)
    after = dataGrab(number, Date2Start, Date2End)
    release_data = release_data_per(before, after, Date1End, Date2Start)
    bat_data = bat_exit_per(before, after, Date1End, Date2Start)

    # comment out to not see avg pitch location & pitch speed
    plot_release_data_per(before, after, Date1End, Date2Start)

    # comment out to not see pitch location by zone graph
    plot_pitch_location(before, after, pFirst, pLast, Date1End, Date2Start)

    # comment out to not see lauch angles
    plot_bat_exit_per(before, after, Date1End, Date2Start)

    data = pd.merge(release_data, bat_data)
    print(data)
    fileName = pFirst + pLast + '.csv'
    data.to_csv(fileName,
                header=True, index=None)
    plt.show()
    input('Enter to Quit.')


if __name__ == "__main__":
    main()
