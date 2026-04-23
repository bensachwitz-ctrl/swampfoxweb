<?php if ( ! defined( 'ABSPATH' ) ) exit; get_header(); ?>

<div class="wrap" style="padding:48px clamp(20px,3vw,48px)">
  <?php if ( have_posts() ) : ?>
    <h1><?php is_home() ? single_post_title() : the_archive_title(); ?></h1>
    <?php while ( have_posts() ) : the_post(); ?>
      <article <?php post_class( 'glass-box' ); ?> style="margin-bottom:24px">
        <header>
          <h2 style="margin:0 0 6px"><a href="<?php the_permalink(); ?>" style="color:var(--forest)"><?php the_title(); ?></a></h2>
          <div style="font-size:.8rem;color:var(--mid);margin-bottom:12px"><?php echo get_the_date(); ?></div>
        </header>
        <?php the_excerpt(); ?>
        <p><a class="btn btn-outline" href="<?php the_permalink(); ?>">Read article →</a></p>
      </article>
    <?php endwhile; ?>
    <?php the_posts_pagination(); ?>
  <?php else : ?>
    <p>No content found.</p>
  <?php endif; ?>
</div>

<?php get_footer(); ?>
