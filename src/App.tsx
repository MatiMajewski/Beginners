import { Navbar } from './components/Navbar';
import { HeroSlider } from './components/HeroSlider';
import { About } from './components/About';
import { Services } from './components/Services';
import { Fleet } from './components/Fleet';
import { Contact } from './components/Contact';
import { Footer } from './components/Footer';

export default function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main id="home" className="pt-20">
        <HeroSlider />
        <About />
        <Services />
        <Fleet />
        <Contact />
      </main>
      <Footer />
    </div>
  );
}
