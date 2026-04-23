<?php if ( ! defined( 'ABSPATH' ) ) exit; get_header(); ?>

<div class="wrap" style="padding:32px clamp(20px,3vw,48px)">
  <?php while ( have_posts() ) : the_post(); ?>
    <div class="sfx-page-content">
      <?php the_content(); ?>
    </div>
  <?php endwhile; ?>
</div>

<?php get_footer(); ?>
