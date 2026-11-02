REQUIRED = {'installation', 'quickstart', 'configuration', 'architecture',
            'testing', 'timeouts', 'retry', 'cancellation', 'limitations'}

def missing_sections(sections):
    return REQUIRED - set(sections)

def test_document_gate():
    assert missing_sections(REQUIRED - {'limitations'}) == {'limitations'}
    assert not missing_sections(REQUIRED)

if __name__ == '__main__':
    test_document_gate()
    print('section presence is necessary, not sufficient; perform the documented steps')
