import { UuidGeneratorRandom } from '../../secondary/uuidGeneratorRandom';

describe('uuid generator', () => {
  it('should generate uuid', () => {
    const sut = new UuidGeneratorRandom();
    // check generate uuid ith regex
    expect(sut.generate()).match(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
  });

  it('should generate different uuid', () => {
    const sut = new UuidGeneratorRandom();
    expect(sut.generate()).not.toEqual(sut.generate());
  });
});
