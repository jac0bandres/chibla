from multiprocessing import Process
import art

import modules.discord_bot as discord_bot
import modules.instagram as instagram


if __name__ == '__main__':
    art.tprint(f"Chinese Blackman")
    print('By zer_el\t\t\t\tA stalker bot for my ex and POC for instaspider project')
    print('Starting processes...')
    instagram_proc = Process(target=instagram.run)
    discord_proc = Process(target=discord_bot.run)

    instagram_proc.start()
    discord_proc.start()

    instagram_proc.join()
    discord_proc.join()