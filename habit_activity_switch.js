let activity = 'Anki created';
let icon;

switch (activity) {
  case 'Article read':
    icon = 'document';
    break;
  case 'Programming sessions':
    icon = 'computer_keyboard';
    break;
  case 'Meditations':
    icon = 'electrical_plug1';
    break;
  case 'Juggling tech sessions':
    icon = 'gears_sc37';
    break;
  case 'Podcast finished':
    icon = 'headset3';
    break;
  case 'Apnea walked':
    icon = 'music_trumpet1';
    break;
  case 'Juggling record broke':
    icon = 'hand22_sc48';
    break;
  case 'Sleep watch':
    icon = 'clock5_sc44';
    break;
  case 'Early phone':
    icon = 'ipod1';
    break;
  case 'Drew':
    icon = 'pen1';
    break;
  case 'Writing sessions':
    icon = 'pencil1';
    break;
  case 'Cold Shower Widget':
    icon = 'snowflake3_sc37';
    break;
  case 'Music listen':
    icon = 'music_eighth_notes';
    break;
  case 'Anki created':
    icon = 'toolset_sc44';
    break;
  case 'Good posture':
    icon = 'robot1';
    break;
  case 'Educational video watched':
    icon = 'computer_monitor';
    break;
  case 'Health learned':
    icon = 'raindrop2';
    break;
  case 'Language studied':
    icon = 'globe';
    break;
  case 'Janki used':
    icon = 'binocular';
    break;
  case 'Apnea practiced':
    icon = 'music_tuba';
    break;
  case 'Anki mydis done':
    icon = 'microscope';
    break;
  case 'Launch Situps Widget':
    icon = 'animal_mouse1';
    break;
  case 'Question asked':
    icon = 'people_couple_sc44';
    break;
  case 'UC post':
    icon = 'wireless';
    break;
  case 'Dream acted':
    icon = 'ship_sc36';
    break;
  case 'Launch Pushups Widget':
    icon = 'animal_lizard1';
    break;
  case 'Todos done':
    icon = 'clipboard1';
    break;
  case 'Apnea spb':
    icon = 'logo_superman_sc37';
    break;
  case 'Apnea apb':
    icon = 'music_microphone';
    break;
  case 'Cardio sessions':
    icon = 'bicycle';
    break;
  case 'Launch Squats Widget':
    icon = 'animal_duck4';
    break;
  case 'Fun juggle':
    icon = 'a_media29_record';
    break;
  default:
    icon = 'Unknown';
}

console.log(`The icon of the ${activity} is ${icon}.`);
