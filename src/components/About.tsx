import { CheckCircle, Award, Users, Truck } from 'lucide-react';

export function About() {
  const stats = [
    { icon: Truck, value: '30+', label: 'Pojazdów w flocie' },
    { icon: Users, value: '100+', label: 'Zadowolonych klientów' },
  ];

  return (
    <section id="about" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl text-gray-900 mb-6">O firmie FM Auto</h2>
            <p className="text-gray-600 mb-6">
              FM Auto to renomowana firma transportowa specjalizująca się w transporcie ciężkim. 
              Oferujemy kompleksowe usługi transportowe z wykorzystaniem nowoczesnej floty lawet i wywrotek.
            </p>
            <p className="text-gray-600 mb-8">
              Nasze wieloletnie doświadczenie, profesjonalna obsługa i nowoczesny park maszynowy 
              gwarantują bezpieczny i terminowy transport Państwa ładunków.
            </p>
            
            <div className="space-y-4">
              {[
                'Terminowość realizacji zleceń',
                'Profesjonalna kadra kierowców',
                'Nowoczesna flota pojazdów',
                'Konkurencyjne ceny',
                'Ubezpieczenie transportu',
                'Obsługa 24/7'
              ].map((item, index) => (
                <div key={index} className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-blue-600 flex-shrink-0" />
                  <span className="text-gray-700">{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="bg-white p-8 rounded-lg shadow-md hover:shadow-lg transition-shadow">
                  <div className="flex items-center gap-4">
                    <div className="bg-blue-100 p-4 rounded-lg">
                      <Icon className="w-8 h-8 text-blue-600" />
                    </div>
                    <div>
                      <div className="text-3xl text-gray-900 mb-1">{stat.value}</div>
                      <div className="text-gray-600">{stat.label}</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
