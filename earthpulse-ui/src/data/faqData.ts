export interface FAQItem {
  q: string;
  a: string;
}

export const FAQS: FAQItem[] = [
  {
    q: "What is EarthPulse AI?",
    a: "EarthPulse AI is a planet-scale environmental intelligence platform that combines satellite imagery, geospatial analytics, and artificial intelligence to detect, track, and visualize environmental changes across the globe.",
  },
  {
    q: "What kind of data does EarthPulse AI use?",
    a: "EarthPulse AI works with multi-source satellite data, including optical satellite imagery, vegetation indices such as NDVI, geospatial vector data (GeoJSON), and time-series environmental datasets. These datasets are processed to generate meaningful insights rather than raw images.",
  },
  {
    q: "What is NDVI and why is it important?",
    a: "NDVI (Normalized Difference Vegetation Index) is a widely used metric that indicates vegetation health and density. It helps identify deforestation, crop stress, land degradation, and environmental recovery over time. EarthPulse AI visualizes NDVI changes using interactive timelines.",
  },
  {
    q: "Is EarthPulse AI a real-time monitoring tool?",
    a: "EarthPulse AI focuses on near-real-time and historical analysis, depending on satellite availability. The platform is designed for trend detection, pattern analysis, and environmental storytelling, not instant surveillance.",
  },
  {
    q: "What can I do in the Dashboard?",
    a: "Inside the Dashboard, users can explore a dark satellite map, scrub through time using an NDVI timeline, inspect environmental events at specific locations, view supporting articles and contextual data, and analyze environmental change visually and interactively.",
  },
  {
    q: "Who is EarthPulse AI for?",
    a: "EarthPulse AI is designed for researchers and scientists, environmental analysts, climate and sustainability teams, policy makers, journalists and storytellers, and developers working with geospatial data.",
  },
  {
    q: "How is EarthPulse AI different from Google Earth?",
    a: "Google Earth focuses on visual exploration. EarthPulse AI focuses on environmental intelligence, combining AI-driven analysis, time-based environmental metrics, event-centric insights, and analytical overlays like NDVI. Think of it as Google Earth + environmental analytics.",
  },
  {
    q: "Do I need technical knowledge to use EarthPulse AI?",
    a: "Basic map interaction requires no technical background. Advanced usage (data interpretation, analysis) benefits from familiarity with environmental or geospatial concepts but is not mandatory.",
  },
  {
    q: "Is EarthPulse AI open-source?",
    a: "The platform architecture is designed to be modular and extensible. Open-source components and datasets may be used, while core intelligence pipelines can remain proprietary depending on deployment.",
  },
  {
    q: "What technologies power EarthPulse AI?",
    a: "EarthPulse AI is built using React + TypeScript, Mapbox GL JS, geospatial data standards (GeoJSON), AI/ML pipelines for data processing, and cloud-based APIs and satellite data services.",
  },
  {
    q: "Can EarthPulse AI be extended or customized?",
    a: "Yes. The platform is designed with extensibility in mind and can be adapted for regional monitoring, custom datasets, research-specific dashboards, and policy and reporting use cases.",
  },
  {
    q: "Is this a production system or a research prototype?",
    a: "EarthPulse AI is built with production-grade frontend architecture and research-driven intelligence pipelines, making it suitable for both applied research and real-world deployments.",
  },
];