import os, sys, pygame, random

def write_schedule(filename, schedule):
    with open(filename, "w") as schedule_file:
        for name in schedule:
            schedule_file.write("%s\n" % name)

class SpeakerIterator:

    def __init__(self, all_speakers):
        self.all_speakers = all_speakers
        self.reset()

    def next(self):
        try:
            self.current_speaker = self.it.next()
        except StopIteration:
            self.reset()
            self.next()

    def reset(self):
        self.it = iter(self.all_speakers.items())

    @property
    def current_name(self):
        return self.current_speaker[0]
    @property
    def current_tile(self):
        return self.current_speaker[1][0]
    @property
    def current_label(self):
        return self.current_speaker[1][1]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(-1)

    number_slots = 96
    slots_per_row = number_slots / 4
    tile_size = 32

    pygame.init()
    screen = pygame.display.set_mode((slots_per_row * tile_size, 600))
    font = pygame.font.SysFont("Comic Sans MS", 20)

    speakers = {}
    for filename in os.listdir("speakers"):
        speakers[filename] = \
            (pygame.image.load("speakers/" + filename),
             font.render(filename, 1, (180, 180, 180)))

    label_selected = font.render("selected speaker:", 1, (100, 100, 100))
    label_all = font.render("all speakers:", 1, (100, 100, 100))

    times = []
    for i in range(9, 17):
        times.append(font.render(str(i), 1, (0, 0, 0)))

    selected_speaker = SpeakerIterator(speakers)
    selected_speaker.next()

    schedule = ["none.png"]* number_slots
    schedule_filename = sys.argv[1]
    with open(schedule_filename) as schedule_file:
        for i, name in enumerate(schedule_file):
            schedule[i] = name.strip("\n")
            print "#", i, name.strip("\n")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_schedule(schedule_filename, schedule)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    selected_speaker.next()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // tile_size, event.pos[1] // tile_size
                i = y * slots_per_row + x
                print i, "set to", selected_speaker.current_name
                if i < len(schedule):
                    schedule[i] = selected_speaker.current_name

        screen.fill((0, 0, 0))
        assert len(schedule) == number_slots
        for i in range(number_slots):
            x = (i % slots_per_row) * tile_size
            y = (i // slots_per_row) * tile_size
            tile_name = schedule[i]
            tile = speakers[tile_name][0]
            screen.blit(tile, (x, y))
        for i, time_label in enumerate(times):
            i *= 12
            x = (i % slots_per_row) * tile_size
            y = (i // slots_per_row) * tile_size
            screen.blit(time_label, (x, y))
        screen.blit(label_all, (10, 195))
        for i, speaker in enumerate(speakers.items()):
            x = 10 + (i // 11) * 200
            y = (i % 11) * tile_size + 220
            screen.blit(speaker[1][0], (x, y))
            screen.blit(speaker[1][1], (x + 40, y))
        screen.blit(label_selected, (10, 135))
        screen.blit(selected_speaker.current_tile, (10, 155))
        screen.blit(selected_speaker.current_label, (50, 155))
        pygame.display.flip()
        pygame.time.wait(100)

