import { UuidGeneratorPort } from '../hexagon/openTask.port';
import { v4 } from 'uuid';

export class UuidGeneratorRandom implements UuidGeneratorPort {
  generate(): string {
    return v4();
  }
}
