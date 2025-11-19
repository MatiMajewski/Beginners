import { Phone, Mail, MapPin, Clock } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';

export function Contact() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    alert('Dziękujemy za wiadomość! Skontaktujemy się z Państwem wkrótce.');
  };

  return (
    <section id="contact" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl text-gray-900 mb-4">Skontaktuj się z nami</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Masz pytania? Potrzebujesz wyceny? Jesteśmy do Twojej dyspozycji!
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          <div>
            <h3 className="text-2xl text-gray-900 mb-6">Dane kontaktowe</h3>
            
            <div className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <Phone className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <div className="text-gray-900 mb-1">Telefon</div>
                  <a href="tel:+48791333246" className="text-blue-600 hover:text-blue-700">
                    +48 791-333-246
                  </a>
                  <br />
                  <a href="tel:+48793333508" className="text-blue-600 hover:text-blue-700">
                    +48 793-333-508
                  </a>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <Mail className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <div className="text-gray-900 mb-1">E-mail</div>
                  <a href="mailto:biuro@fmauto.pl" className="text-blue-600 hover:text-blue-700">
                    biuro@fmauto.pl
                  </a>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <MapPin className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <div className="text-gray-900 mb-1">Adres</div>
                  <div className="text-gray-600">
                    ul. Grunwaldzka 6<br />
                    84-230 Rumia<br />
                    Polska
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <Clock className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <div className="text-gray-900 mb-1">Godziny otwarcia</div>
                  <div className="text-gray-600">
                    Poniedziałek - Piątek: 8:00 - 16:00
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-2xl text-gray-900 mb-6">Formularz kontaktowy</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Input
                  type="text"
                  placeholder="Imię i nazwisko"
                  required
                  className="w-full"
                />
              </div>
              <div>
                <Input
                  type="email"
                  placeholder="Adres e-mail"
                  required
                  className="w-full"
                />
              </div>
              <div>
                <Input
                  type="tel"
                  placeholder="Numer telefonu"
                  required
                  className="w-full"
                />
              </div>
              <div>
                <Input
                  type="text"
                  placeholder="Temat"
                  required
                  className="w-full"
                />
              </div>
              <div>
                <Textarea
                  placeholder="Wiadomość"
                  required
                  rows={6}
                  className="w-full"
                />
              </div>
              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
                Wyślij wiadomość
              </Button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
}
