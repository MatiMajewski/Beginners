import { Facebook, Instagram, Linkedin, Mail, Phone } from 'lucide-react';
import logoImage from 'figma:asset/d5c10190b238435b384d373cfbebd41b9180f513.png';

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="mb-4">
              <img src={logoImage} alt="FM Auto" className="h-10" />
            </div>
            <p className="text-gray-400 text-sm">
              Profesjonalne usługi transportowe lawetami i wywrotkami na terenie całej Polski i Europy.
            </p>
          </div>

          <div>
            <h4 className="text-white mb-4">Szybkie linki</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#home" className="text-gray-400 hover:text-blue-400 transition-colors">Strona główna</a></li>
              <li><a href="#about" className="text-gray-400 hover:text-blue-400 transition-colors">O nas</a></li>
              <li><a href="#services" className="text-gray-400 hover:text-blue-400 transition-colors">Usługi</a></li>
              <li><a href="#fleet" className="text-gray-400 hover:text-blue-400 transition-colors">Flota</a></li>
              <li><a href="#contact" className="text-gray-400 hover:text-blue-400 transition-colors">Kontakt</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white mb-4">Usługi</h4>
            <ul className="space-y-2 text-sm">
              <li className="text-gray-400">Transport lawetami</li>
              <li className="text-gray-400">Transport wywrotkami</li>
              <li className="text-gray-400">Transport międzynarodowy</li>
              <li className="text-gray-400">Transport ekspresowy</li>
              <li className="text-gray-400">Usługi spedycyjne</li>
            </ul>
          </div>

          <div>
            <h4 className="text-white mb-4">Kontakt</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-center gap-2 text-gray-400">
                <Phone className="w-4 h-4" />
                +48 791-333-246
              </li>
              <li className="flex items-center gap-2 text-gray-400">
                <Phone className="w-4 h-4" />
                +48 793-333-508
              </li>
              <li className="flex items-center gap-2 text-gray-400">
                <Mail className="w-4 h-4" />
                biuro@fmauto.pl
              </li>
            </ul>
            <div className="flex gap-3 mt-6">
              <a href="#" className="bg-gray-800 hover:bg-blue-600 p-2 rounded-lg transition-colors">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="bg-gray-800 hover:bg-blue-600 p-2 rounded-lg transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="bg-gray-800 hover:bg-blue-600 p-2 rounded-lg transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
          <p>&copy; 2025 FM Auto. Wszelkie prawa zastrzeżone.</p>
        </div>
      </div>
    </footer>
  );
}
