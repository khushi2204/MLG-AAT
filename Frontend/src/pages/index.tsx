import Head from 'next/head';
import FileUpload from './components/FileUpload';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Sign Language Detection</title>
        <meta name="description" content="Sign Language Detection using Machine Learning" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header>
        <h1>Sign Language Detection</h1>
      </header>

      <main>
        <FileUpload />
      </main>

      <footer>
        <p>&copy; 2024 Sign Language Detection. All Rights Reserved.</p>
      </footer>
    </div>
  );
}