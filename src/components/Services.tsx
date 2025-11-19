import { Truck, Container, Package, MapPin, Clock, Shield } from 'lucide-react';

export function Services() {
  const services = [
    {
      icon: Truck,
      title: 'Transport Lawetami',
      description: 'Specjalizujemy się w transporcie samochodów osobowych i małych busów. Dysponujemy małymi lawetami z naczepą oraz dużymi lawetami z lory, dostosowanymi do Państwa potrzeb.'
    },
    {
      icon: Container,
      title: 'Transport Wywrotkami',
      description: 'Profesjonalny transport materiałów sypkich, gruzu, piasku, żwiru i innych materiałów budowlanych. Dysponujemy wywrotkami o różnej pojemności.'
    },
    {
      icon: MapPin,
      title: 'Transport Krajowy i Międzynarodowy',
      description: 'Realizujemy zlecenia transportowe w całej Polsce oraz w krajach Unii Europejskiej. Zapewniamy szybką i bezpieczną dostawę.'
    },
    {
      icon: Clock,
      title: 'Transport Ekspresowy',
      description: 'Pilne zlecenia? Oferujemy usługi transportu ekspresowego z gwarancją terminowości i elastycznością w planowaniu.'
    },
    {
      icon: Package,
      title: 'Usługi Spedycyjne',
      description: 'Kompleksowa obsługa spedycyjna, organizacja transportu, dokumentacja celna i międzynarodowa koordynacja dostaw.'
    },
    {
      icon: Shield,
      title: 'Pełne Ubezpieczenie',
      description: 'Wszystkie przewożone ładunki są objęte ubezpieczeniem cargo, co gwarantuje bezpieczeństwo Państwa majątku.'
    }
  ];

  return (
    <section id="services" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl text-gray-900 mb-4">Nasze usługi</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Oferujemy kompleksowe rozwiązania transportowe dostosowane do indywidualnych potrzeb każdego klienta
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => {
            const Icon = service.icon;
            return (
              <div 
                key={index}
                className="bg-gray-50 p-8 rounded-lg hover:shadow-lg transition-all hover:-translate-y-1"
              >
                <div className="bg-blue-100 w-16 h-16 rounded-lg flex items-center justify-center mb-6">
                  <Icon className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-xl text-gray-900 mb-3">{service.title}</h3>
                <p className="text-gray-600">{service.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
