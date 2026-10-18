export const SITE_NAME = 'Print & Play Game';
export const SITE_URL = 'https://printandplaygame.com';

export function pageTitle(t: string): string {
  return t.includes(SITE_NAME) ? t : `${t} | ${SITE_NAME}`;
}
export function breadcrumbLd(items: { name: string; href: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({ '@type': 'ListItem', position: i + 1, name: it.name, item: SITE_URL + it.href })),
  };
}
export function faqLd(faq: { q: string; a: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })),
  };
}
export function collectionLd(name: string, url: string, items: { name: string; url: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name,
    url: SITE_URL + url,
    mainEntity: { '@type': 'ItemList', itemListElement: items.slice(0, 50).map((it, i) => ({ '@type': 'ListItem', position: i + 1, name: it.name, url: SITE_URL + it.url })) },
  };
}
