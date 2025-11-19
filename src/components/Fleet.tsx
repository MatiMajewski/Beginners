import fleetImage1 from 'figma:asset/bab6b72950a285f99e775291b9da5a4e38e5760b.png';
import fleetImage2 from 'figma:asset/88b05e3e89df070cb396342f3718241f9f78dd4b.png';

export function Fleet() {
  const vehicles = [
    {
      type: 'Lawety',
      models: [
        'Małe lawety z naczepą',
        'Duże lawety z lory',
        'Transport samochodów osobowych',
        'Transport małych busów'
      ],
      capacity: 'Różne konfiguracje',
      image: fleetImage1
    },
    {
      type: 'Ciężarówki',
      models: [
        'Transport międzynarodowy',
        'Transport krajowy',
        'Pojazdy z naczepą',
        'Nowoczesna flota Mercedes'
      ],
      capacity: 'Różne konfiguracje',
      image: fleetImage2
    }
  ];

  return (
    <section id="fleet" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl text-gray-900 mb-4">Nasza flota</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Dysponujemy nowoczesnym parkiem maszynowym, regularnie serwisowanym i dostosowanym do najbardziej wymagających zleceń
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {vehicles.map((vehicle, index) => (
            <div key={index} className="bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
              <div className="h-64 relative">
                <img
                  src={vehicle.image}
                  alt={vehicle.type}
                  className="w-full h-full object-cover"
                />
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-4 py-2 rounded-lg">
                  {vehicle.capacity}
                </div>
              </div>
              <div className="p-8">
                <h3 className="text-2xl text-gray-900 mb-4">{vehicle.type}</h3>
                <ul className="space-y-2">
                  {vehicle.models.map((model, idx) => (
                    <li key={idx} className="flex items-center text-gray-600">
                      <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
                      {model}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 bg-blue-600 text-white rounded-lg p-8 text-center">
          <h3 className="text-2xl mb-4">Cała flota jest wyposażona w:</h3>
          <div className="grid md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div>
              <div className="mb-2">🛰️</div>
              <div>System GPS</div>
            </div>
            <div>
              <div className="mb-2">📱</div>
              <div>Łączność online</div>
            </div>
            <div>
              <div className="mb-2">🔒</div>
              <div>Systemy zabezpieczeń</div>
            </div>
            <div>
              <div className="mb-2">✅</div>
              <div>Aktualne przeglądy</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
