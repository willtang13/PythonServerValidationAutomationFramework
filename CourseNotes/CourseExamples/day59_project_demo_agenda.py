AGENDA = [('problem', 40), ('architecture', 70), ('failure-demo', 70),
          ('evidence', 60), ('limitations', 60)]

def test_agenda():
    assert sum(seconds for _, seconds in AGENDA) == 300
    assert any(topic == 'limitations' for topic, _ in AGENDA)

if __name__ == '__main__':
    test_agenda()
    for topic, seconds in AGENDA:
        print(f'{topic}: {seconds}s')
